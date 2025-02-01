import requests
import time


class ProxyManager:
    def __init__(self, proxy_url=None, max_retries=3, retry_delay=60, request_timeout=10):
        """
        Manages HTTP requests with optional proxy and retry mechanism
        """
        self.proxies = {"https": proxy_url} if proxy_url else None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.request_timeout = request_timeout

    def route_request(self, url):
        """
        Makes a GET request via proxy with retry mechanism
        """
        retries = 0
        response = None
        while retries < self.max_retries:
            try:
                response = requests.get(url, proxies=self.proxies, timeout=self.request_timeout)
                # Raise exception for HTTP errors (4xx, 5xx)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {retries + 1}/{self.max_retries}): {e}")
                # Check if response exists and is a site server error (5xx)
                if response and response.status_code >= 500:
                    retries += 1
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    # Don't retry for non-server errors (4xx errors)
                    break
        print("Failed to fetch data after multiple retries")
        return None
