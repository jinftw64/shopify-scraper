import requests
import json

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

def main():
    shopify_url = input("Enter the Shopify store URL (e.g., https://examplestore.myshopify.com/): ")
    products = scrape_shopify_products(shopify_url)

    if products:
        print(f"Successfully scraped {len(products)} products.")
        # Save products to a JSON file
        with open('shopify_products.json', 'w') as f:
            json.dump(products, f, indent=4)
        print("Products saved to shopify_products.json")
    else:
        print("No products found or failed to scrape the store.")

if __name__ == "__main__":
    main()
