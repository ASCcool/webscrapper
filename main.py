import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import ScrapeRequest
from notification import NotificationManager
from scraper import Scraper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_TOKEN = os.getenv("API_SECRET_TOKEN")
PRODUCT_PAGE_BASE_URL = os.getenv("PRODUCT_PAGE_BASE_URL")

# Start FastAPI app
app = FastAPI()
security = HTTPBearer()


def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate API token
    """
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Token")


@app.get("/")
def home():
    """
    Landing Page
    """
    return {"message": "Welcome to Proxied Scraper Tool!"}


@app.post("/scrape")
def scrape_products(
    request: ScrapeRequest,
    credentials: HTTPAuthorizationCredentials = Depends(authenticate_token),
):
    """
    Scrape products with provided settings
    """

    print(f"Scraping {request.pages} pages...")

    scraper = Scraper(base_url=PRODUCT_PAGE_BASE_URL, proxy_url=request.proxy_url)
    notifier = NotificationManager(send_email=request.send_email)

    all_products = []
    for page in range(1, request.pages + 1):
        print(f"Scraping page {page}...")
        products = scraper.scrape_page(page)
        all_products.extend(products)

    updated_count = len(all_products)

    # Send notification if required
    if updated_count > 0:
        notifier.send_notification(updated_count, request.pages)

    return {
        "message": f"Scraped {updated_count} products across {request.pages} pages and updated the DB"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
