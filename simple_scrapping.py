import os
import requests
from bs4 import BeautifulSoup


# Function to download images
def download_image(url, folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the image name from the URL
            image_name = os.path.join(folder, url.split('/')[-1].split('?')[0])
            with open(image_name, 'wb') as file:
                file.write(response.content)
            print(f'Downloaded: {image_name}')
    except Exception as e:
        print(f'Could not download {url}. Reason: {e}')


# Function to scrape images from a webpage
def scrape_contents(url, limit=50):
    # Create a folder to save images
    folder = 'downloaded_images'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    product_items = soup.find_all('div', class_='product-item')
    products = []
    for item in product_items:
        link_tag = item.find('img').attrs['src']
        title_tag = item.find('div', class_='product-title')
        price_tag = item.find('div', class_='price')
        product_detail = {
            "product-name": title_tag.contents[0],
            "product_link": link_tag,
            "price_tag": price_tag.contents[0].contents[0]
        }
        products.append(product_detail)


# Example usage
if __name__ == '__main__':
    scrape_contents('https://www.gofynd.com/products')
