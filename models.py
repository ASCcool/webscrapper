from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class Product(BaseModel):
    product_title: str
    product_price: int
    product_url: HttpUrl
    product_image: HttpUrl


class ScrapeRequest(BaseModel):
    pages: int = Field(1, gt=0, description="Number of pages to scrape")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL for requests")
    send_email: bool = Field(False, description="Send an email notification after scraping")
