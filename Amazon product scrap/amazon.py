from datetime import datetime
import requests
import csv
from bs4 import BeautifulSoup

USER_AGENT= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

def get_page_html(url):
    res = requests.get(url=url, headers= REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs= {
        'class': 'a-price a-text-price a-size-medium apexPriceToPay'
    })
    if main_price_span:
        price_spans = main_price_span.findAll('span')
        for span in price_spans:
            price = span.text.strip().replace('$', '').replace(',', '')
            if price:  # If a valid price is found, return it
                return price
    return None  # Return None if no price is found

def get_product_title(soup):
    product_title = soup.find('span', id='productTitle')
    return product_title.text.strip()

def get_product_rating(soup):
    get_product_ratings_div = soup.find('div', attrs= {
        'id': 'averageCustomerReviews'
    })

    product_rating_section = get_product_ratings_div.find('i', attrs={
        'class': 'a-icon-star'
    })
    product_rating_span = product_rating_section.find('span')
    try:
        rating = product_rating_span.text.strip().split()
        
        return float(rating[0])
    except ValueError:
        print("value obtained cannot be passed")
        exit()

def get_product_technical_details(soup):
    details = {}
    technical_details_section = soup.find('div', id='prodDetails')
    data_tables = technical_details_section.findAll('table', class_='prodDetTable')
    for table in data_tables:
        table_rows = table.findAll('tr')
        for row in table_rows:
            row_key = row.find('th').text.strip()
            row_value = row.find('td').text.strip().replace('\u200e', '')
            details[row_key] = row_value
    return details

def extract_product_info(url):
    product_info = {}
    print(f'scraping URL: {url}')
    html = get_page_html(url)
    soup = BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))
    return product_info


if __name__ == "__main__":
    products_data = []
    with open('amazon_products_urls_.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            products_data.append(extract_product_info(url))

output_file_name = 'output-{}.csv'.format(datetime.today().strftime("%m-%d-%Y"))
with open(output_file_name, 'w') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(products_data[0].keys())
    for product in products_data:
        writer.writerow(product.values())