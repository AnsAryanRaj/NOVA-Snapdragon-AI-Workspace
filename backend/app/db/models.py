"""Database Models for NOVA Audit Trail and Tool Registry."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.db.database import Base


class AuditLogEntry(Base):
    """Stores audit logs for all executed system tool actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    action_name = Column(String(100), nullable=False)
    tool_name = Column(String(100), nullable=False, index=True)
    parameters_json = Column(Text, nullable=True)
    requires_confirmation = Column(Boolean, default=True)
    user_confirmed = Column(Boolean, default=False)
    status = Column(String(50), nullable=False)  # 'SUCCESS', 'REJECTED', 'FAILED'
    execution_time_ms = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)


class RegisteredTool(Base):
    """Stores metadata for explicitly registered system tools."""
    __tablename__ = "registered_tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)  # 'file', 'document', 'system_utility', 'voice', 'vision'
    description = Column(Text, nullable=False)
    is_destructive = Column(Boolean, default=False)
    requires_confirmation = Column(Boolean, default=True)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentModel(Base):
    """Stores metadata and status for indexed workspace documents."""
    __tablename__ = "documents"

    id = Column(String(64), primary_key=True, index=True)  # Deterministic doc_id
    relative_path = Column(String(500), unique=True, nullable=False, index=True)
    file_name = Column(String(255), nullable=False, index=True)
    file_extension = Column(String(20), nullable=False)
    mime_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    content_hash = Column(String(64), nullable=False)
    page_count = Column(Integer, default=1)
    chunk_count = Column(Integer, default=0)
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    extraction_status = Column(String(50), default="SUCCESS", nullable=False)
    error_message = Column(Text, nullable=True)


class DocumentChunkModel(Base):
    """Stores extracted text chunks for document retrieval and search."""
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chunk_id = Column(String(100), unique=True, nullable=False, index=True)
    doc_id = Column(String(64), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    start_char = Column(Integer, nullable=False, default=0)
    end_char = Column(Integer, nullable=False, default=0)
    page_number = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

