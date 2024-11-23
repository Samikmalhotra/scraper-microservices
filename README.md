# Scraper Microservices
A simple microservices app which processes inter service communication using redis pubsub and scrapes company data from *https://search.sunbiz.org/*

## Prerequisites
-   Python 3.8 or later
-   Node.js and npm (for React client)
-   Redis
-   Docker 

## Features

-   **Scraper App**: Handles scraping tasks triggered by the server.
-   **Server App**: Acts as a central API gateway to communicate with the scraper and serve data to the React client.
-   **Redis Pub/Sub**: Enables efficient communication between `server` and `scraper` via message channels.
-   **React Client**: Provides a user-friendly interface for interacting with the server API.

## Installation
### 1. Clone the repository
```
git clone https://github.com/Samikmalhotra/scraper-microservices.git
cd scraper-microservices`
```
> Note: Instead of following the  next steps, you can just run the *setup.sh* script present in this directory:
> ```
> chmod 777 setup.sh
> ./setup.sh
> ```

### 2. Setup DB
```
docker  run  --name  postgres-db  -e  POSTGRES_USER=postgres  -e  POSTGRES_PASSWORD=password  -e  POSTGRES_DB=db  -p  5432:5432  -d  postgres
```
### 3. Setup Redis Server
```
docker  run  --name  redis-server  -p  6380:6379  -d  redis
```

### 4. Setup Scraper Service
```
cd  ./scraper
python  -m  venv  venv
source  venv/bin/activate
pip  install  --upgrade  pip
pip  install  -r  requirements.txt
python  run.py
```

### 5. Setup Server Service
```
cd  ./server
python  -m  venv  venv
source  venv/bin/activate
pip  install  --upgrade  pip
pip  install  -r  requirements.txt
python  run.py
```
### 6. Setup Client App
```
cd  ./client
npm  install
npm  run  dev
```

# API Documentation

## Server


The server app acts as the central API gateway, handling requests from the React client and coordinating communication with the scraper app via Redis.
It is also the only service that interacts with the database

#### Redis Listener
When the service is started, it listens to a channel `data` and whenever a message is received on this channel, the data is saved to database or updated if already present.

#### Base URL  

The server app runs at:  
`http://localhost:5001` 

---

#### **1. `/get_data_by_document_number`**  

**Description**:  
Fetches data for a specific document number.  

**Workflow**
- Searches the db for exisiting data present for the document number
- If data not found or data was last updated over an hour ago then publishes a message on a redis channel `scrape_request` to scrape the data
- Listens to the response for the request on the channel `scrape_response`
- Maps the response into json and replies


**Method**:  
`POST`  

**Request Body**:  
The request body must be in JSON format.  

```json  
{
  "document_number": "<string>"
}
```

#### **2. `/get_history`**

**Description**:  
Retrieves the history of previously processed document numbers ordered by the document that was last accessed.

**Workflow**
- Fetches all the documents accessed in the order of last accessed.
- Maps response to json and replies

**Method**:  
`GET`

**Request Parameters**:  
None.

## Scraper Service  

The scraper service is responsible for scraping data from the website: *https://search.sunbiz.org/* based on requests received from the server app.  

### Redis Listener
When the service is started, it listens to a channel `scrape_request` and whenever a message is received on this channel, it scrapes the data based on the request and emits response on the channel `data`

### Base URL  

The scraper service runs at:  
`http://localhost:5000` 

---

####  **1. `/scrape_data_by_entity_name`**  

**Description**:  
Scrapes data for a specific entity name and gives a list of all entities/companies matching the name.

**Workflow**
- Scrapes the data to find the companies matching the given name
- Sends a list of companies along with document number and status

> Note: Their is no persistence with respect to data processed by this endpoint

**Method**:  
`POST`  

**Request Body**:  
The request body must be in JSON format.  

```json  
{
  "entity_name": "<string>"
}
```

#### **2. `/scrape_data_by_document_number`**
> This is an auxiliary endpoint not being used in the running app

**Description**:  
Scrapes data for a specific document number

**Workflow**
- Scrapes the data to find the details for the given document number
- Emits a message on the redis channel `data` with the scraped data
- Sends the scraped data in the form of json

**Method**:  
`POST`

**Request Body**:  
The request body must be in JSON format.

```json  
{
  "document_number": "<string>"
}
```