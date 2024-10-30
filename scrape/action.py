import copy
import json
import os
import httpx
from httpx import RequestError, HTTPStatusError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import requests
from bs4 import BeautifulSoup

from common.notification_manager import ConsoleNotification
from config import current_config
from scrape.helper import ScrapeStorage


class SrapeDataHunter:

    IMAGE_DIR = "images"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COUNT_PRODUCT_SCRAPED = 0
    COUNT_PRODUCTS_STORAGE = 0

    def write_details(self, products):
        file_path = os.path.join(self.BASE_DIR, "product.json")
        with open(file_path, 'w') as outfile:
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

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RequestError, HTTPStatusError))
    )
    async def fetch_page(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return response

    async def store_scrape_contents(self, db_products):
        storage_class = ScrapeStorage(current_config.mongo_db_client, current_config.redis_db_client)
        storage_class.preprocess_data(db_products)
        await storage_class.trigger_storage_pipeline()
        self.COUNT_PRODUCT_SCRAPED = len(db_products)
        self.COUNT_PRODUCTS_STORAGE = storage_class.products_updated

    def notify_scrape_content(self):
        notification_class = ConsoleNotification()
        message = {"products_scraped": self.COUNT_PRODUCT_SCRAPED, "products_updated": self.COUNT_PRODUCTS_STORAGE}
        notification_class.notify(message)
        return message

    async def scrape_contents(self, base_url, limit=10):
        products = list()
        db_products = list()
        for page_no in range(1, limit+1):
            if page_no == 1:
                url = base_url
            else:
                url = f"{base_url}/page/{page_no}/"
            response = await self.fetch_page(url)

            soup = BeautifulSoup(response.content, 'html.parser')
            product_box_div = soup.find('div', attrs={"id": "mf-shop-content"}).find('ul', attrs={"class": "products columns-4"})
            product_items = product_box_div.find_all('li', recursive=False)

            for counter, item in enumerate(product_items):
                image_tag = item.find('div', attrs={"class": "mf-product-thumbnail"}).find('a').find('img')
                title_tag = item.find('h2').find('a')
                price_tag = item.find('bdi')

                price = float(price_tag.contents[1])
                product_unique_id = title_tag.attrs['href'].split('/')[-2]
                image_url = image_tag.attrs['data-lazy-src']
                product_title = title_tag.contents[0]

                image_path = os.path.join(self.BASE_DIR, self.IMAGE_DIR, os.path.basename(image_url.split('/')[-1]))
                self.download_image(image_url=image_url, image_path=image_path)
                absolute_path = os.path.abspath(image_path)
                product_detail = {
                    "title": product_title,
                    "image_path": absolute_path,
                    "price": price
                }
                products.append(product_detail)
                product_detail_db = copy.deepcopy(product_detail)
                product_detail_db.update({"id": product_unique_id})
                db_products.append(product_detail_db)
        self.write_details(products)
        await self.store_scrape_contents(db_products)
        message = self.notify_scrape_content()
        return message


# Example usage
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SrapeDataHunter().scrape_contents('https://dentalstall.com/shop', limit=3))
