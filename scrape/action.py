import json
import os

import redis
# from app import mongo_db_client
# from app import redis_db_client
import requests
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient

from scrape.helper import ScrapeStorage


class SrapeDataHunter:

    IMAGE_DIR = "images"

    def write_details(self, products):
        file_name = './products.json'
        with open(file_name, 'w') as outfile:
            json.dump(products, outfile, indent=4)

    def download_image(self, image_url, image_path):
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        try:
            response = requests.get(image_url)
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {image_url}: {e}")

    async def scrape_contents(self, url, limit=10):
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        product_items = soup.find_all('div', class_='product-item',  limit=limit)
        products = []
        db_products = []
        for item in product_items:
            link_tag = item.find('img').attrs['src']
            title_tag = item.find('div', class_='product-title')
            price_tag = item.find('div', class_='price')
            product_unique_id = item.find('a').attrs['href'].split('-')[-1]
            image_url = link_tag
            image_path = os.path.join(self.IMAGE_DIR, os.path.basename(image_url.split('/')[-1]))
            self.download_image(image_url=link_tag, image_path=image_path)
            absolute_path = os.path.abspath(image_path)
            price = price_tag.contents[0].contents[0].replace("₹", "").strip().replace(',', '').strip()
            product_detail = {
                "title": title_tag.contents[0],
                "image_path": absolute_path,
                "price": price
            }
            products.append(product_detail)
            product_detail_db = {
                "title": title_tag.contents[0],
                "image_path": absolute_path,
                "price": price,
                "id": product_unique_id
            }
            db_products.append(product_detail_db)
        self.write_details(products)
        mongo_db_client = AsyncIOMotorClient("mongodb://localhost:27017")
        redis_db_client = redis.Redis.from_url('redis://localhost:6379')
        storage_class = ScrapeStorage(mongo_db_client, redis_db_client)
        storage_class.preprocess_data(db_products)
        await storage_class.trigger_storage_pipeline()


# Example usage
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SrapeDataHunter().scrape_contents('https://www.gofynd.com/products'))
