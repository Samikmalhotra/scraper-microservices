from flask import Blueprint, jsonify, request
from app import db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from app.controllers import *


bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return jsonify("Scraper service is running!")

@bp.route('/get_data_by_entity_name', methods=['POST'])
def get_result_by_entity_name():
    entity_name = request.json.get('entity_name')
    try:
        return get_result_by_entity_name_controller(entity_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/get_data_by_document_number', methods=['POST'])
def get_result_by_document_number():
    document_number = request.json.get('document_number')
    try:
        return get_result_by_document_number_controller(document_number)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



