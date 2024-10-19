import requests
import json
import os

def scrape_shopify_products(shopify_url):
    # Normalize URL to ensure it ends with a slash
    if not shopify_url.endswith('/'):
        shopify_url += '/'

    # Construct the URL to fetch products in JSON format
    products_url = f"{shopify_url}products.json?limit=250"
    products = []
    page = 1

    while True:
        response = requests.get(products_url + f"&page={page}")
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break

        data = response.json()
        if 'products' not in data or len(data['products']) == 0:
            break

        products.extend(data['products'])
        page += 1

    return products

def download_product_images(products):
    # Create a directory to store product images
    if not os.path.exists('product_images'):
        os.makedirs('product_images')

    for product in products:
        product_id = product['id']
        product_title = product['title'].replace('/', '_')  # Replace slashes to avoid directory issues
        product_dir = os.path.join('product_images', f"{product_id}_{product_title}")

        if not os.path.exists(product_dir):
            os.makedirs(product_dir)

        images = product.get('images', [])
        for index, image in enumerate(images):
            image_url = image['src']
            image_extension = image_url.split('.')[-1]
            image_path = os.path.join(product_dir, f"image_{index + 1}.{image_extension}")

            try:
                img_data = requests.get(image_url).content
                with open(image_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded image for product '{product_title}' at {image_path}")
            except Exception as e:
                print(f"Failed to download image {image_url}: {e}")

def main():
    shopify_url = input("Enter the Shopify store URL (e.g., https://examplestore.myshopify.com/): ")
    products = scrape_shopify_products(shopify_url)

    if products:
        print(f"Successfully scraped {len(products)} products.")
        # Save products to a JSON file
        with open('shopify_products.json', 'w') as f:
            json.dump(products, f, indent=4)
        print("Products saved to shopify_products.json")

        # Download product images
        download_product_images(products)
    else:
        print("No products found or failed to scrape the store.")

if __name__ == "__main__":
    main()
