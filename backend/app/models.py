from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, ForeignKey, Float
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
    rdf_generations = relationship("RDFGeneration", back_populates="user")

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
    cytoscape_files = relationship("CytoscapeFile", back_populates="identifier_set")
    rdf_generations = relationship("RDFGeneration", back_populates="identifier_set")


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

class CytoscapeFile(Base):
    __tablename__ = "cytoscape_files"
    id = Column(Integer, primary_key=True, index=True)
    identifier_set_id = Column(Integer, ForeignKey("identifier_sets.id"))
    cytoscape_graph = Column(JSON, nullable=True)
    status = Column(String)
    error_message = Column(String, nullable=True)


    identifier_set = relationship("IdentifierSet", back_populates="cytoscape_files")

class RDFFile(Base):
    __tablename__ = "rdf_files"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    type = Column(String, nullable=False)  # RDF, SHACL, UML
    created_at = Column(DateTime, default=datetime.utcnow)

class RDFGeneration(Base):
    __tablename__ = "rdf_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    identifier_set_id = Column(Integer, ForeignKey("identifier_sets.id"), nullable=False)
    graph_name = Column(String, nullable=False)
    base_uri = Column(String, nullable=False)
    version_iri = Column(String, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    creators = Column(JSON, nullable=False)  # List of {"full_name": str, "orcid": str}
    generate_shacl = Column(Boolean, default=True)
    shacl_threshold = Column(Float, default=0.001)
    generate_uml_diagram = Column(Boolean, default=True)
    generate_shex = Column(Boolean, default=True)
    shex_threshold = Column(Float, default=0.001)
    generated_files = Column(JSON)  # Store the list of generated files
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="rdf_generations")
    identifier_set = relationship("IdentifierSet", back_populates="rdf_generations")