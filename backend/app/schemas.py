from pydantic import BaseModel, EmailStr, Extra, Field
from typing import Optional, Dict, List
from datetime import datetime

# User Authentication Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    preferences: Optional[Dict] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class UserInfo(BaseModel):
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    api_key: str
    map_name: str
    is_active: bool
    preferences: Dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    token: str
    user: UserInfo

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Identifier Processing Schemas
class IdentifierInput(BaseModel):
    identifier_type: str
    text_input: Optional[str] = None
    file_content: Optional[str] = None
    input_species: str = "Human"

class MappedIdentifier(BaseModel):
    identifier: str
    identifier_source: str
    target: str
    target_source: str


class IdentifierMappingResponse(BaseModel):
    id: int
    identifier_type: str
    input_species: str
    input_identifiers: List[str]
    mapped_identifiers: Optional[Dict[str, MappedIdentifier]] = None  # Changed to Dict
    mapped_identifiers_subset: Optional[Dict[str, MappedIdentifier]] = None
    bridgedb_metadata: Optional[Dict] = None
    mapped_identifiers_list: Optional[List[str]] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IdentifierProcessingResponse(BaseModel):
    set_id: int
    status: str
    message: str
    warnings: Optional[List[str]] = None

# Data Source Schemas
class DataSourceInfo(BaseModel):
    name: str
    description: str
    requires_key: bool
    requires_map_name: bool
    base_url: str

class DataSourceRequest(BaseModel):
    source: str
    api_key: Optional[str] = None
    map_name: Optional[str] = None

class ProcessDataSourcesRequest(BaseModel):
    datasources: List[DataSourceRequest]

class DataSourceResponse(BaseModel):
    id: str
    name: str
    description: str
    requires_key: bool
    requires_map_name: bool


class CombinedAnnotation(BaseModel):
    identifier: str
    identifier_source: str = Field(..., alias="identifier.source")
    target: str
    target_source: str = Field(..., alias="target.source")

    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True

class DataSourceProcessingResponse(BaseModel):
    identifier_set_id: int
    combined_df: Optional[Dict[str, CombinedAnnotation]] = None  # Changed to Dict
    combined_metadata: Optional[List[Dict]] = None
    opentargets_df: Optional[Dict[str, CombinedAnnotation]] = None  # Changed to Dict
    captured_warnings: Optional[List[str]] = None
    # pygraph: Optional[Dict] = None
    mapped_identifiers_list: Optional[List[str]] = None
    status: str
    error_message: Optional[str] = None
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class DataSourceRequest(BaseModel):
    source: str
    api_key: Optional[str] = None
    map_name: Optional[str] = None

# Combined Data Result Schemas
class NodeData(BaseModel):
    id: str
    type: str
    label: str
    properties: Optional[Dict] = None

class EdgeData(BaseModel):
    source: str
    target: str
    type: str
    weight: Optional[float] = None
    properties: Optional[Dict] = None

class NetworkData(BaseModel):
    nodes: List[NodeData]
    edges: List[EdgeData]
    metadata: Dict

class VisualizationResponse(BaseModel):
    network_data: NetworkData
    source_metadata: Dict
    statistics: Dict

    class Config:
        from_attributes = True