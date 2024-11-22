import redis
import json
from app.models import *
from sqlalchemy.exc import SQLAlchemyError

def listen_to_redis(redis_client: redis.StrictRedis, app_context):
    pubsub = redis_client.pubsub()
    pubsub.subscribe('data')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = (message['data'])
            try:
                parsed_data = json.loads(data)
                print("Received data length:", len(parsed_data))
                save_data_to_db(parsed_data, app_context)
            except json.JSONDecodeError:
                print("Received data is not valid JSON.")

def save_data_to_db(data, app_context):
    print("Saving data to database...")
    with app_context:
        for item in data:
            print(f"Processing data for {item.get('document_number')}...")
            try:
                entity = Entity.query.filter_by(document_number=item.get("document_number")).first()

                if entity:
                    print(f"Updating data for {item.get('document_number')}...")
                    entity.name = item.get("name", entity.name)
                    entity.status = item.get("status", entity.status)
                    entity.fei_number = item.get("fei_number", entity.fei_number) if item.get("FEI/EIN Number") != "NONE" else entity.fei_number
                    entity.date_filed = item.get("date_filed", entity.date_filed)
                    entity.state = item.get("state", entity.state)
                    entity.last_event = item.get("last_event", entity.last_event)
                    entity.event_date_filed = item.get("event_date_filed", entity.event_date_filed)
                    entity.event_effective_date = item.get("event_effective_date", entity.event_effective_date)
                    entity.principal_address = item.get("principal_address", entity.principal_address)
                    entity.mailing_address = item.get("mailing_address", entity.mailing_address)
                    entity.registered_agent = item.get("registered_agent", entity.registered_agent)
                    entity.registered_agent_address = item.get("registered_agent_address", entity.registered_agent_address)
                else:
                    entity = Entity(
                        document_number=item.get("document_number", None),
                        name=item.get("name", None),
                        status=item.get("status", None),
                        fei_number=item.get("fei_number", None) if item.get("FEI/EIN Number") != "NONE" else None,
                        date_filed=item.get("date_filed", None),
                        state=item.get("state", None),
                        last_event=item.get("last_event", None),
                        event_date_filed=item.get("event_date_filed", None),
                        event_effective_date=item.get("event_effective_date", None),
                        principal_address=item.get("principal_address", None),
                        mailing_address=item.get("mailing_address", None),
                        registered_agent=item.get("registered_agent", None),
                        registered_agent_address=item.get("registered_agent_address", None),
                    )
                    db.session.add(entity)

                officers = item.get("officers", [])
                for officer in officers:
                    officer_record = Officers.query.filter_by(document_number=item["document_number"], name=officer["name"]).first()
                    if not officer_record:
                        officer_record = Officers(
                            document_number=item["document_number"],
                            name=officer["name"],
                            title=officer["title"],
                            address=officer["address"]
                        )
                        db.session.add(officer_record)

                document_images = item.get("document_images", [])
                for image in document_images:
                    document_image_record = DocumentImages.query.filter_by(document_number=item["document_number"], title=image["title"]).first()
                    if not document_image_record:
                        document_image_record = DocumentImages(
                            document_number=item["document_number"],
                            link=image["link"],
                            title=image["title"]
                        )
                        db.session.add(document_image_record)

                reports = item.get("annual_reports", [])
                for report in reports:
                    annual_report_record = AnnualReports.query.filter_by(document_number=item["document_number"], report_year=report["report_year"]).first()
                    if not annual_report_record:
                        annual_report_record = AnnualReports(
                            document_number=item["document_number"],
                            report_year=report["report_year"],
                            filed_date=report.get("filed_date")
                        )
                        db.session.add(annual_report_record)

                db.session.commit()

                print(f"Data for {item.get('document_number')} saved successfully.")

            except SQLAlchemyError as e:
                db.session.rollback()

                print(f"Error occurred: {str(e)}")

            finally:
                db.session.close()