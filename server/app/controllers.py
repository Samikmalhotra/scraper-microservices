from flask import jsonify
from app.models import Entity
from app.utils import *


def get_all_companies():
    try:
        entities = Entity.query.order_by(Entity.last_accessed_time.desc()).all()
        if not entities:
            return jsonify([]), 200

        return jsonify(map_entities(entities))

    except Exception as e:
        raise e
    
def get_result_by_document_number_controller(document_number):
    try:
        entity = Entity.query.filter_by(document_number=document_number).first()
        entity = [entity] if entity else None
        if entity:
            update_last_accessed(entity[0])
        elif not entity or was_last_accessed_over_an_hour_ago(entity[0]):
            print("Scraping data...")
            data = get_scraped_data(document_number)
            print(data)
            if 'error' in data:
                return jsonify(data), 500
            print("Entity scraped")
            entity = data
            
        if entity is None:
            print("Entity is None")
            return jsonify({'error': 'An error occured'}), 500
        
        return jsonify(map_entities(entity))

    except Exception as e:
        raise e
