from flask import Blueprint, jsonify, request
from app import db
from app.controllers import *

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return jsonify("Server is running!")    

@bp.route('/get_history', methods=['GET'])
def get_history():
    try:
        return get_all_companies()
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

@bp.route('/get_data_by_document_number', methods=['POST'])
def get_result_by_document_number():
    document_number: str = request.json.get('document_number')
    print(document_number)
    try:
        return get_result_by_document_number_controller(document_number)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

