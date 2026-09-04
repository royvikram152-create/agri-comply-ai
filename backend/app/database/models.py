from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, Enum as SQLEnum, JSON
from datetime import datetime
import uuid
from app.database.database import Base

class ShipmentDB(Base):
    __tablename__ = "shipments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tracking_number = Column(String, unique=True, index=True)
    crop = Column(String, nullable=False)
    variety = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    deadline_days = Column(Integer, nullable=False)
    status = Column(String, default="CREATED")
    compliance_score = Column(Float, default=0.0)
    risk_level = Column(String, default="MEDIUM")
    exporter_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    shipment_id = Column(String, index=True)
    document_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    status = Column(String, default="PENDING")
    issue_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    extracted_fields = Column(JSON, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class AuditEventDB(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    shipment_id = Column(String, index=True)
    event_type = Column(String, nullable=False)
    agent_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ApprovalDB(Base):
    __tablename__ = "approvals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    shipment_id = Column(String, index=True)
    reviewer = Column(String, nullable=False)
    action = Column(String, nullable=False)
    comments = Column(Text, nullable=True)
    previous_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
