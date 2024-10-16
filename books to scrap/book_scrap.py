import requests
from bs4 import BeautifulSoup
import csv

response = requests.get(url= "https://books.toscrape.com/")

page_source = (response.content)
soup = BeautifulSoup(page_source, 'html.parser')

heading_elements = (soup.find_all('h3'))
pricing_elements = soup.find_all('p', {'class': 'price_color'})

complete_data = []

for each_heading, each_pricing_element in zip(heading_elements, pricing_elements):
    book_name = (each_heading.get_text()) #returns each book name

    each_link = each_heading.find('a')
    
    book_link = (each_link.get('href')) #fetches url link


# print(pricing_elements)
    book_price = (each_pricing_element.get_text())
    
    complete_data.append ({'book_name': book_name, 'book_price': book_price, 'book_link': book_link})

csv_filename = 'scrapped_books.csv'

fieldNames = ['book_name', 'book_price', 'book_link']

with open (csv_filename, 'w', newline= "", encoding= 'utf-8') as csv_file:
    csv.DictWriter(csv_file, fieldnames=fieldNames).writerows(complete_data)