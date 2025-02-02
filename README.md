# Welcome to Proxied Webscraper Tool!

This project is a Python-based web scraper built using FastAPI, BeautifulSoup, and Redis to extract product details from [`dentalstall.com`](https://dentalstall.com/shop/). It stores the scraped data in JSON files, caches results in Redis, and downloads product images for local storage.

---

## **Features**
- Scrapes product **name, price, and image** from multiple pages.
- Supports **pagination** while scraping (scrapes from first `N` pages).
- Supports use of **external proxy** for making requests.
- Stores data in **JSON format**, allowing easy extension to a database.
- **Downloads images locally** and saves the path in JSON.
- Implements **Redis caching** for pricing data to prevent unnecessary updates.
- **Retries failed requests** (e.g., due to server errors).
- Requires **API authentication** using a static token.
- Sends **notifications** upon completion of job via **console** and **email**.

---

## **Setup & Installation**

### **1. Clone the Repository**
```sh
git clone https://github.com/ASCcool/webscrapper.git
cd webscraper
```

### **2. Set Up Virtual Environment**
```sh
# The project was developed using Python 3.8.19
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
```sh
# Put these contents inside .env 
API_SECRET_TOKEN=<your_api_token>
PRODUCT_PAGE_BASE_URL=https://dentalstall.com/shop/page/
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=<gmail-app-password>
NOTIFICATION_EMAIL=recipient-email@gmail.com
```

## **Running the Application**

### **1. Start Redis Server**
```sh
# Ensure liveness of redis server
redis-server 
```

### **2. Run the FastAPI Server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://127.0.0.1:8000
