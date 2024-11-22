import app.RedisClientSingleton as RedisClientSingleton
import json
import time
from app.models import Entity
from datetime import datetime, timezone, timedelta
from app import db

def map_entities(entities):
    print("Mapping entities...")
    companies_data = []

    for company in entities:
        company_data = {}

        company_data['document_number'] = get_attr(company, 'document_number')
        company_data['name'] = get_attr(company, 'name')
        company_data['fei_ein_number'] = get_attr(company, 'fei_number')
        company_data['state'] = get_attr(company, 'state')
        company_data['status'] = get_attr(company, 'status')
        company_data['address'] = get_attr(company, 'principal_address')
        company_data['mailing_address'] = get_attr(company, 'mailing_address')
        company_data['registered_agent'] = get_attr(company, 'registered_agent')
        company_data['registered_agent_address'] = get_attr(company, 'registered_agent_address')
        company_data['last_event'] = get_attr(company, 'last_event')
        company_data['event_date_filed'] = get_attr(company, 'event_date_filed')
        company_data['event_effective_date'] = get_attr(company, 'event_effective_date')
        company_data['date_filed'] = get_attr(company, 'date_filed')

        officers_data = []
        officers = get_attr(company, 'officers', [])
        for officer in officers:
            officer_data = {
                'name': get_attr(officer, 'name'),
                'title': get_attr(officer, 'title'),
                'address': get_attr(officer, 'address')
            }
            officers_data.append(officer_data)
        company_data['officers'] = officers_data

        annual_reports_data = []
        annual_reports = get_attr(company, 'annual_reports', [])
        for report in annual_reports:
            report_data = {
                'filed_date': get_attr(report, 'filed_date'),
                'year': get_attr(report, 'report_year')
            }
            annual_reports_data.append(report_data)
        company_data['annual_reports'] = annual_reports_data

        document_images_data = []
        document_images = get_attr(company, 'document_images', [])
        for doc_image in document_images:
            document_image_data = {
                'link': get_attr(doc_image, 'link'),
                'title': get_attr(doc_image, 'title')
            }
            document_images_data.append(document_image_data)
        company_data['document_images'] = document_images_data

        companies_data.append(company_data)

    return companies_data

def get_attr(obj, attr, default=None):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def get_scraped_data(document_number: str):
    redis_client = RedisClientSingleton.get_instance()
    print("Publishing scrape request...")
    redis_client.publish("scrape_request", document_number)

    start_time = time.time()
    print("Waiting for scrape response started at ", start_time)
    pubsub = redis_client.pubsub()
    pubsub.subscribe("scrape_response")
    while True:
        if time.time() - start_time > 30:
            pubsub.unsubscribe("scrape_response")
            raise TimeoutError(f"Timeout: No response received within 30 seconds.")
        
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            if message['type'] == 'message':
                pubsub.unsubscribe("scrape_response")
                data = json.loads(message['data'])
                return data
                
def update_last_accessed(entity: Entity):
    print("Updating last accessed time...")
    entity.last_accessed_time = datetime.now(timezone.utc)
    db.session.commit()

def was_last_accessed_over_an_hour_ago(entity):
    if entity.last_accessed_time:
        if entity.last_accessed_time < datetime.now(timezone.utc) - timedelta(hours=1):
            return True
    return False

