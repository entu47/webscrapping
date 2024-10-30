# **Web Scraping API with FastAPI**
A FastAPI-based API for scraping content from websites, retrieving and storing data, and serving it through RESTful endpoints.

## **TABLE OF CONTENTS**
* [Overview](#overview)
* Technologies Used
* Installation
* Running The Application
* API Endpoints

# **OVERVIEW**
This API is built with FastAPI to scrape content from websites and store it database and cache. It allows clients to fetch data from specified websites and returns the information about scraped content. This API can be integrated with various applications or used as a standalone service for content retrieval and monitoring.

# **TECHNOLOGIES USED**
* FAST API
* BEAUTIFUL SOUP
* UVICORN
* MONGODB
* REDIS

# **INSTALLATION**

## **Prerequisites**

* Python 3.11+
* Poetry

## **Steps**

1. Clone the repository:
   1. git clone git@github.com:entu47/webscrapping.git
   2. cd webscrapping
2. Install dependencies:
   1. poetry install


# **RUNNING THE APPLICATION**
## **Start the FastAPI Server**
uvicorn app:app

# **API ENDPOINT**

| Endpoint     | Method | Descrption              |
|--------------|--------|-------------------------|
| /v1.0/scrape | POST   | Initiates the scraping. |

## /v1.0/scrape Endpoint Details
### **Headers**
* It has got two custom headers:
  * X-Application-ID = morningstar
  * X-Application-Token = 311E6D8D5C295512CE4BC6BBD413F

#### Example Request:

`{
    "url":"https://dentalstall.com/shop",
    "limit": 2
}`
#### Sample Response:
* 200
   * `{
        "success": true,
        "products_scraped": 24,
        "products_updated": 0
    }`
   
