import os
import tempfile
import uuid
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import pandas as pd
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from pyBiodatafuse.graph.rdf import BDFGraph
from pyBiodatafuse.graph.rdf.graphdb import GraphDBManager

from ..models import RDFFile
from .. import models
from ..schemas import RDFGenerationResponse, GeneratedFile


class RDFService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.temp_dir = Path(tempfile.gettempdir()) / "biodatafuse_rdf"
        self.temp_dir.mkdir(exist_ok=True)
        self.generated_files = {}  # In-memory for legacy, but not used for persistence

    async def persist_file(self, file_id, user_id, name, path, type_):
        # Check if already exists
        stmt = select(RDFFile).where(RDFFile.id == file_id)
        result = await self.db.execute(stmt)
        if not result.scalar_one_or_none():
            rdf_file = RDFFile(
                id=file_id,
                user_id=user_id,
                name=name,
                path=path,
                type=type_,
                created_at=datetime.utcnow()
            )
            self.db.add(rdf_file)
            await self.db.commit()

    async def get_file_info(self, file_id: str, user_id: int = None) -> Optional[Dict]:
        # Always fetch from DB
        stmt = select(RDFFile).where(RDFFile.id == file_id)
        result = await self.db.execute(stmt)
        rdf_file = result.scalar_one_or_none()
        if rdf_file and (user_id is None or rdf_file.user_id == user_id):
            return {
                "id": rdf_file.id,
                "name": rdf_file.name,
                "path": rdf_file.path,
                "type": rdf_file.type,
                "user_id": rdf_file.user_id,
            }
        return None

    async def generate_rdf_graph(
        self,
        identifier_set_id: int,
        base_uri: str,
        version_iri: str,
        author_name: str,
        author_email: str,
        orcid: str,
        graph_name: str,
        generate_shacl: bool = True,
        shacl_threshold: float = 0.001,
        generate_uml_diagram: bool = True,
        user_id: int = None,
    ) -> RDFGenerationResponse:
        """Generate RDF graph from annotation data."""
        
        # Get identifier set and annotations
        result = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == identifier_set_id)
        )
        identifier_set = result.scalar_one_or_none()
        
        if not identifier_set:
            raise ValueError("Identifier set not found")
        
        if user_id and identifier_set.user_id != user_id:
            raise ValueError("Not authorized to access this identifier set")
        
        # Get annotation data
        result = await self.db.execute(
            select(models.Annotation).where(models.Annotation.identifier_set_id == identifier_set_id)
        )
        annotation = result.scalar_one_or_none()
        
        if not annotation or not annotation.combined_df:
            raise ValueError("No annotation data found for this identifier set")
        
        # Convert data to DataFrame
        combined_df = pd.DataFrame.from_dict(annotation.combined_df, orient='index')
        combined_metadata = annotation.combined_metadata or []
        
        # Create BDFGraph instance
        bdf = BDFGraph(
            base_uri=base_uri,
            version_iri=version_iri,
            orcid=orcid,
            author=author_name,
        )
        
        # Generate RDF
        bdf.generate_rdf(combined_df, combined_metadata)
        
        # Create unique directory for this generation
        generation_id = str(uuid.uuid4())
        output_dir = self.temp_dir / generation_id
        output_dir.mkdir(exist_ok=True)

        generated_files = []

        # Serialize RDF graph
        rdf_file_path = output_dir / f"{graph_name}.ttl"
        bdf.serialize(str(rdf_file_path), format="ttl")
        file_id = str(uuid.uuid4())
        self.generated_files[file_id] = {
            "name": f"{graph_name}.ttl",
            "path": str(rdf_file_path),
            "type": "RDF",
            "user_id": user_id,
            "created_at": datetime.now()
        }
        # Persist to DB
        await self.persist_file(file_id, user_id, f"{graph_name}.ttl", str(rdf_file_path), "RDF")
        generated_files.append(GeneratedFile(
            id=file_id,
            name=f"{graph_name}.ttl",
            type="RDF",
            size=rdf_file_path.stat().st_size
        ))

        # Generate SHACL if requested
        if generate_shacl:
            try:
                shacl_file_path = output_dir / f"{graph_name}_shacl.ttl"
                uml_file_path = None
                if generate_uml_diagram:
                    uml_file_path = output_dir / f"{graph_name}_shacl.png"
                bdf.shacl(
                    path=str(shacl_file_path),
                    threshold=shacl_threshold,
                    uml_figure_path=str(uml_file_path) if uml_file_path else None,
                )
                # Add SHACL file
                shacl_file_id = str(uuid.uuid4())
                self.generated_files[shacl_file_id] = {
                    "name": f"{graph_name}_shacl.ttl",
                    "path": str(shacl_file_path),
                    "type": "SHACL",
                    "user_id": user_id,
                    "created_at": datetime.now()
                }
                await self.persist_file(shacl_file_id, user_id, f"{graph_name}_shacl.ttl", str(shacl_file_path), "SHACL")
                generated_files.append(GeneratedFile(
                    id=shacl_file_id,
                    name=f"{graph_name}_shacl.ttl",
                    type="SHACL",
                    size=shacl_file_path.stat().st_size
                ))
                # Add UML diagram if generated
                if uml_file_path and uml_file_path.exists():
                    uml_file_id = str(uuid.uuid4())
                    self.generated_files[uml_file_id] = {
                        "name": f"{graph_name}_shacl.png",
                        "path": str(uml_file_path),
                        "type": "UML",
                        "user_id": user_id,
                        "created_at": datetime.now()
                    }
                    await self.persist_file(uml_file_id, user_id, f"{graph_name}_shacl.png", str(uml_file_path), "UML")
                    generated_files.append(GeneratedFile(
                        id=uml_file_id,
                        name=f"{graph_name}_shacl.png",
                        type="UML",
                        size=uml_file_path.stat().st_size
                    ))
            except Exception as e:
                print(f"Warning: SHACL generation failed: {e}")
                # Continue without SHACL

        # Store BDF graph object for GraphDB operations (in-memory only)
        self.generated_files[f"{generation_id}_bdf"] = {
            "bdf_graph": bdf,
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return RDFGenerationResponse(
            generation_id=generation_id,
            generated_files=generated_files,
            message="RDF graph generated successfully"
        )

    async def get_bdf_graph(self, generation_id: str, user_id: int = None) -> Optional[BDFGraph]:
        """Get BDF graph object by generation ID."""
        bdf_key = f"{generation_id}_bdf"
        file_info = self.generated_files.get(bdf_key)
        
        if not file_info:
            return None
        
        if user_id and file_info.get("user_id") != user_id:
            return None
        
        return file_info.get("bdf_graph")
