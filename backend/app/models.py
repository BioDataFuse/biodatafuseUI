from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PickleType

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
    identifier_set = relationship("IdentifierSet", back_populates="user")

class IdentifierSet(Base):
    __tablename__ = "identifier_sets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    identifier_type = Column(String)
    input_species = Column(String, default="Human")
    input_identifiers = Column(JSON)
    mapped_identifiers = Column(JSON, nullable=True)
    mapped_identifiers_subset = Column(JSON, nullable=True)
    bridgedb_metadata = Column(JSON, nullable=True)
    mapped_identifiers_list = Column(JSON, nullable=True)
    status = Column(String)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="identifier_set")
    annotation = relationship("Annotation", back_populates="identifier_set")


class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True, index=True)
    identifier_set_id = Column(Integer, ForeignKey("identifier_sets.id"))
    combined_df = Column(JSON, nullable=True)
    combined_metadata = Column(JSON, nullable=True)
    opentargets_df = Column(JSON, nullable=True)
    # pygraph = Column(PickleType, nullable=True)
    captured_warnings = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)

    identifier_set = relationship("IdentifierSet", back_populates="annotation")


class RDFFile(Base):
    __tablename__ = "rdf_files"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    type = Column(String, nullable=False)  # RDF, SHACL, UML
    created_at = Column(DateTime, default=datetime.utcnow)