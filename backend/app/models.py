from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True, index=True)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    identifier_sets = relationship("IdentifierSet", back_populates="user")

class IdentifierSet(Base):
    __tablename__ = "identifier_sets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    identifier_type = Column(String)
    input_species = Column(String, default="Human")
    input_identifiers = Column(JSON)  # Store the original identifiers
    mapped_identifiers = Column(JSON, nullable=True)  # Store the mapped identifiers
    mapped_identifiers_subset = Column(JSON, nullable=True)  # Store the subset of mapped identifiers
    bridgedb_metadata = Column(JSON, nullable=True)  # Store the BridgeDB metadata
    mapped_identifiers_list = Column(JSON, nullable=True)  # Store the identifiers that were mapped
    status = Column(String)  # pending, processing, completed, error
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="identifier_sets")