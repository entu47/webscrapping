import json
import requests
from bs4 import BeautifulSoup
from scrape.helper import update_scrape_details_in_db


class SrapeDataHunter:

    def write_details(products):
        file_name = '../products.json'
        with open(file_name, 'w') as outfile:
            json.dump(products, outfile, indent=4)

    def scrape_contents(url, limit=150):

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        product_items = soup.find_all('div', class_='product-item',limit=limit)
        products = []
        for item in product_items:
            link_tag = item.find('img').attrs['src']
            title_tag = item.find('div', class_='product-title')
            price_tag = item.find('div', class_='price')
            product_detail = {
                "name": title_tag.contents[0],
                "link": link_tag,
                "price": price_tag.contents[0].contents[0].replace("₹", "").strip()
            }
            products.append(product_detail)
        write_details(products)
        update_scrape_details_in_db(products)


# Example usage
if __name__ == '__main__':
    scrape_contents('https://www.gofynd.com/products')
