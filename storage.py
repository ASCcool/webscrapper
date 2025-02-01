import os
import json
import redis
import hashlib
import requests


def generate_md5_hash(product_url):
    return hashlib.md5(product_url.encode()).hexdigest()


class StorageManager:
    def __init__(self, storage_type="json"):
        """
        Initialize storage with Redis cache and directory setup
        """
        self.storage_type = storage_type
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.base_directory = os.path.join(os.path.dirname(__file__), "data")

    def save(self, data, page=1):
        """
        Save product data as individual JSON files under data/page_<id>
        Updates are made only if price has changed, data cached in Redis
        """
        page_directory = os.path.join(self.base_directory, f"page_{page}")
        image_directory = os.path.join(page_directory, "images")
        os.makedirs(page_directory, exist_ok=True)
        os.makedirs(image_directory, exist_ok=True)

        updated_count, updated_products = 0, []

        for product in data:
            # Determine product uniqueness using its URL
            product_url = str(product["product_url"]).strip()
            product_id = generate_md5_hash(product_url)
            filename = os.path.join(page_directory, f"{product_id}.json")

            old_price = self.redis_client.get(product_id)
            old_price = int(old_price) if old_price else 0
            new_price = product["product_price"]

            # Skip if price is the same
            if old_price and old_price == new_price:
                continue
            else:
                print(f"Price updated for product_id: {product_id}, old_price: {str(old_price)} and new_price: {new_price}")

            self.redis_client.set(product_id, new_price)

            # Download image and update local image path
            product["path_to_image"] = self.save_image(product["product_image"], product_id, image_directory)

            # Convert HttpUrl to string before saving
            product["product_url"] = str(product["product_url"])
            product["product_image"] = str(product["product_image"])

            # Save product info json
            self.__save_json__(product, filename)

            updated_count += 1
            updated_products.append(product)

        print(f"Updated {updated_count} products on page {page}")
        return updated_products

    def save_image(self, image_url, product_id, image_directory):
        """
        Download and save product image locally
        """
        if not image_url or image_url == "N/A":
            return ""
        try:
            response = requests.get(image_url, stream=True, timeout=10)
            response.raise_for_status()
            image_path = os.path.join(image_directory, f"{product_id}.jpg")
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            return image_path
        except requests.RequestException:
            print(f"Failed to download image for {product_id}. Keeping original URL.")
            return ""

    def __save_json__(self, data, filename):
        """
        Save product data as an individual JSON file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
