import re
from models import Product
from bs4 import BeautifulSoup
from proxy import ProxyManager
from storage import StorageManager


def format_price(price_str):
    """
    Remove currency symbols and convert price to integer
    """
    price_str = re.sub(r"[^\d.]", "", price_str)
    return int(float(price_str))


class Scraper:
    def __init__(self, base_url, proxy_url=None):
        """
        Initialize scraper with ProxyManager and StorageManager
        """
        self.base_url = base_url
        self.storage = StorageManager()
        # All requests are routed via Proxy manager instance
        self.proxy_manager = ProxyManager(proxy_url)

    def fetch_page(self, page_number):
        """
        Fetch HTML content via ProxyManager
        """
        url = f"{self.base_url}{page_number}/"
        print("url:", url)
        return self.proxy_manager.route_request(url)

    def parse_products(self, html_content):
        """
        Parse products from the given HTML content
        """
        soup = BeautifulSoup(html_content, "html.parser")
        products = soup.find_all("li", class_="product")
        extracted_products = []

        # For every product, we now parse the html response tag by tag to find relevant attributes
        for product in products:
            title_tag = product.find("h2", class_="woo-loop-product__title")
            product_title = title_tag.get_text(strip=True) if title_tag else "N/A"

            url_tag = title_tag.find("a") if title_tag else None
            product_url = url_tag["href"] if url_tag else "N/A"

            img_tag = product.find("img", class_="attachment-woocommerce_thumbnail")
            product_image = img_tag["data-lazy-src"] if img_tag and "data-lazy-src" in img_tag.attrs else "N/A"

            price_tag = product.find("span", class_="woocommerce-Price-amount")
            product_price = format_price(price_tag.get_text(strip=True)) if price_tag else 0

            # Ensure scraped data is validated using pydantic
            try:
                product_data = Product(
                    product_title=product_title,
                    product_price=product_price,
                    product_url=product_url,
                    product_image=product_image
                )
                extracted_products.append(product_data.dict())  # Convert to dict for storage
            except Exception as e:
                print(f"Data validation failed for {product_title}: {e}")

        return extracted_products

    def scrape_page(self, page_number):
        """
        Scrape a given page and save the results
        """
        html_content = self.fetch_page(page_number)
        if html_content:
            products = self.parse_products(html_content)
            updated_products = self.storage.save(products, page=page_number)
            return updated_products
        return []


if __name__ == "__main__":
    args = {
        "base_url": "https://dentalstall.com/shop/page/",
        "proxy_url": None
    }
    scraper = Scraper(**args)
    scraper.scrape_page(1)
