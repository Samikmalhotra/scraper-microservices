from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class Entity(db.Model):
    __tablename__ = 'entity'
    document_number = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    fei_number = db.Column(db.String(80), nullable=True)
    date_filed = db.Column(db.String(80), nullable=True)
    state = db.Column(db.String(80), nullable=True)
    last_event = db.Column(db.String(80), nullable=True)
    event_date_filed = db.Column(db.String(80), nullable=True)
    event_effective_date = db.Column(db.String(80), nullable=True)
    principal_address = db.Column(db.String(250), nullable=True)
    mailing_address = db.Column(db.String(250), nullable=True)
    registered_agent = db.Column(db.String(250), nullable=True)
    registered_agent_address = db.Column(db.String(250), nullable=True)
    last_accessed_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    annual_reports = db.relationship('AnnualReports', backref='entity', lazy=True)
    officers = db.relationship('Officers', backref='entity', lazy=True)
    document_images = db.relationship('DocumentImages', backref='entity', lazy=True)

class AnnualReports(db.Model):
    __tablename__ = 'annual_reports'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    document_number = db.Column(db.String(80), db.ForeignKey('entity.document_number'), nullable=False)
    report_year = db.Column(db.String(80), nullable=False)
    filed_date = db.Column(db.String(80), nullable=True)

class Officers(db.Model):
    __tablename__ = 'officers'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    document_number = db.Column(db.String(80), db.ForeignKey('entity.document_number'), nullable=False)
    name = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(250), nullable=True)

class DocumentImages(db.Model):
    __tablename__ = 'document_images'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    document_number = db.Column(db.String(80), db.ForeignKey('entity.document_number'), nullable=False)
    link = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(80), nullable=False)
