import os
import tempfile
import uuid
import json
import logging
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

# Add logger
logger = logging.getLogger(__name__)

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
        generate_shex: bool = True,
        shex_threshold: float = 0.001,
        user_id: int = None,
    ) -> RDFGenerationResponse:
        """Generate RDF graph from annotation data."""
        try:
            logger.info(f"🚀 Starting RDF generation for identifier_set_id: {identifier_set_id}")
            
            # Get identifier set and annotations
            result = await self.db.execute(
                select(models.IdentifierSet).where(models.IdentifierSet.id == identifier_set_id)
            )
            identifier_set = result.scalar_one_or_none()
            
            if not identifier_set:
                logger.error(f"❌ Identifier set {identifier_set_id} not found")
                raise ValueError("Identifier set not found")
            
            if user_id and identifier_set.user_id != user_id:
                logger.error(f"❌ User {user_id} not authorized to access identifier set {identifier_set_id}")
                raise ValueError("Not authorized to access this identifier set")
            
            # Get annotation data
            result = await self.db.execute(
                select(models.Annotation).where(models.Annotation.identifier_set_id == identifier_set_id)
            )
            annotation = result.scalar_one_or_none()
            
            if not annotation or not annotation.combined_df:
                logger.error(f"❌ No annotation data found for identifier set {identifier_set_id}")
                raise ValueError("No annotation data found for this identifier set")
            
            logger.info(f"📊 Found annotation data, converting to DataFrame...")
            
            # Convert data to DataFrame
            combined_df = pd.DataFrame.from_dict(annotation.combined_df, orient='index')
            combined_metadata = annotation.combined_metadata or []
            
            logger.info(f"🧬 Creating BDFGraph instance...")
            
            # Create BDFGraph instance
            bdf = BDFGraph(
                base_uri=base_uri,
                version_iri=version_iri,
                orcid=orcid,
                author=author_name,
            )
            
            logger.info(f"📈 Generating RDF from annotation data...")
            
            # Generate RDF
            bdf.generate_rdf(combined_df, combined_metadata)
            
            # Create unique directory for this generation
            generation_id = str(uuid.uuid4())
            output_dir = self.temp_dir / generation_id
            output_dir.mkdir(exist_ok=True)

            logger.info(f"📁 Created output directory: {output_dir}")

            generated_files = []

            # Serialize RDF graph
            rdf_file_path = output_dir / f"{graph_name}.ttl"
            logger.info(f"💾 Serializing RDF graph to: {rdf_file_path}")
            
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

            logger.info(f"✅ RDF graph serialized successfully")

            # Generate SHACL if requested
            if generate_shacl:
                try:
                    logger.info(f"🔍 Generating SHACL shapes with threshold: {shacl_threshold}")
                    
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
                    
                    logger.info(f"✅ SHACL shapes generated successfully")
                    
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
                        
                        logger.info(f"✅ UML diagram generated successfully")
                        
                except Exception as e:
                    logger.warning(f"⚠️ SHACL generation failed: {e}")
                    # Continue without SHACL

            # Generate ShEx shapes if requested
            if generate_shex:
                try:
                    logger.info(f"📐 Generating ShEx shapes with threshold: {shex_threshold}")
                    
                    shex_file_id = str(uuid.uuid4())
                    shex_filename = f"{graph_name}_shex.ttl"
                    shex_path = output_dir / shex_filename
                    
                    # Generate ShEx with UML diagram
                    uml_shex_path = None
                    if generate_uml_diagram:
                        uml_shex_path = output_dir / f"{graph_name}_shex_diagram.png"
                    
                    bdf.shex(
                        path=str(shex_path),
                        threshold=shex_threshold,
                        uml_figure_path=str(uml_shex_path) if uml_shex_path else None
                    )
                    
                    # Store ShEx file
                    shex_size = shex_path.stat().st_size
                    await self.persist_file(shex_file_id, user_id, shex_filename, str(shex_path), "ShEx")
                    
                    generated_files.append(GeneratedFile(
                        id=shex_file_id,
                        name=shex_filename,
                        type="ShEx",
                        size=shex_size
                    ))
                    
                    logger.info(f"✅ ShEx shapes generated successfully")
                    
                    # Store ShEx UML diagram if generated
                    if uml_shex_path and uml_shex_path.exists():
                        shex_uml_id = str(uuid.uuid4())
                        shex_uml_filename = f"{graph_name}_shex_diagram.png"
                        shex_uml_size = uml_shex_path.stat().st_size
                        await self.persist_file(shex_uml_id, user_id, shex_uml_filename, str(uml_shex_path), "ShEx_UML")
                        
                        generated_files.append(GeneratedFile(
                            id=shex_uml_id,
                            name=shex_uml_filename,
                            type="ShEx_UML",
                            size=shex_uml_size
                        ))
                        
                        logger.info(f"✅ ShEx UML diagram generated successfully")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to generate ShEx: {str(e)}")
                    # Continue without ShEx

            # Store BDF graph object for GraphDB operations (in-memory only)
            self.generated_files[f"{generation_id}_bdf"] = {
                "bdf_graph": bdf,
                "user_id": user_id,
                "created_at": datetime.now()
            }

            logger.info(f"🎉 RDF generation completed successfully. Generated {len(generated_files)} files")

            return RDFGenerationResponse(
                generation_id=generation_id,
                generated_files=generated_files,
                message="RDF graph generated successfully"
            )
            
        except Exception as e:
            logger.error(f"❌ Error generating RDF graph: {str(e)}")
            raise

    async def get_bdf_graph(self, generation_id: str, user_id: int = None) -> Optional[BDFGraph]:
        """Get BDF graph object by generation ID."""
        try:
            # Try to get from memory first
            key = f"{generation_id}_bdf"
            if key in self.generated_files:
                file_data = self.generated_files[key]
                if user_id is None or file_data.get("user_id") == user_id:
                    return file_data.get("bdf_graph")
            
            # If not in memory, we would need to reconstruct it from stored data
            # For now, return None - this indicates the graph needs to be regenerated
            logger.warning(f"BDF graph with generation_id '{generation_id}' not found in memory")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving BDF graph: {str(e)}")
            return None
