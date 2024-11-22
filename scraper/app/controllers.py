from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.RedisClientSingleton import RedisClientSingleton
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.scraper import *

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--remote-debugging-port=9222") 

def get_result_by_entity_name_controller(entity_name: str):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        return jsonify({'error': 'Failed to initiate driver'}), 500
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://search.sunbiz.org/Inquiry/CorporationSearch/ByName")
    input_field = driver.find_element(By.ID, "SearchTerm")
    input_field.send_keys(entity_name)
    input_field.submit()
    
    try:
        search_results = driver.find_element(By.ID, "search-results")
        return jsonify(handle_multiple_search_results(driver))
    except:
        raise e
    finally:
        driver.quit()

def get_result_by_document_number_controller(document_number: str):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        raise e

    wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException])

    driver.get("https://search.sunbiz.org/Inquiry/CorporationSearch/ByDocumentNumber")

    input_field = wait.until(EC.presence_of_element_located((By.ID, "SearchTerm")))
    # driver.find_element(By.ID, "SearchTerm")
    input_field.send_keys(document_number)
    input_field.submit()

    try:
        single_search_result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchResultDetail")))
        print("Single search result found")
        data = handle_single_search_result(single_search_result)
        print(data)
        print("Data scraped" )  

        redis_client = RedisClientSingleton.get_instance()
        redis_client.publish("data", json.dumps(data))

        return data
    except TimeoutException:
        try:
            validation_error = driver.find_element(By.CLASS_NAME, "validation-summary-errors")
            if validation_error:
                print("Document not found")
                raise Exception("Search result not found")
        except NoSuchElementException:
            raise Exception("Search result not found and validation error not displayed.")
    except Exception:
        raise Exception("An error occured while scraping the document number: " + document_number)
    finally:
        driver.quit()