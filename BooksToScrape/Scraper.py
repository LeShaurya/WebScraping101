import requests
import lxml
from bs4 import BeautifulSoup
import json
import re

def scrape_book_info(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.text, 'lxml')
    productMain = soup.select_one('.col-sm-6.product_main')        
    
    book_title = soup.select_one('h1').text
    book_description = soup.select_one('.product_page > p').text
    
    pattern = re.compile(r'star-rating.(\w+)')

    matching_paragraphs = productMain.find(class_ = pattern)
    rating = matching_paragraphs['class'][1]        
    
    tableData = {}
    # get data from individual rows of header and data
    table = soup.select_one('.table.table-striped')
    for row in table.select('tr'):
        key = row.th.text.strip()
        value = row.td.text.strip()
        tableData[key] = value
    
    book_info = {'Title': book_title, 'Description': book_description, 'Rating':rating, 'BookInformation': tableData}
    
    return book_info

if __name__ == "__main__":
    baseUrl = 'https://books.toscrape.com/catalogue/page-{}.html'    
    
    booksList = list()
    for i in range(1,51):
        pageUrl = baseUrl.format(i)
        response = requests.get(pageUrl)
        soup = BeautifulSoup(response.text, 'lxml')
        
        books = soup.find_all(class_='product_pod')
        for book in books:
            book_link = 'https://books.toscrape.com/catalogue/' + book.find('a')['href']
            book_description = scrape_book_info(book_link)        
            booksList.append(book_description)
    json_data = json.dumps(booksList, indent=2,ensure_ascii=False)
    
    print(json_data)
