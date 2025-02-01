from pydantic import BaseModel, EmailStr
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

class IdentifierMappingResponse(BaseModel):
    id: int
    identifier_type: str
    input_species: str
    input_identifiers: List[str]
    mapped_identifiers: Optional[List] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IdentifierProcessResponse(BaseModel):
    set_id: int
    status: str
    message: str
    warnings: Optional[List[str]] = None

# Data Source Schemas
class DataSourceInfo(BaseModel):
    name: str
    description: str
    requires_key: bool

class DataSourceRequest(BaseModel):
    source: str
    api_key: Optional[str] = None

class ProcessDataSourcesRequest(BaseModel):
    datasources: List[DataSourceRequest]

class DataSourceResponse(BaseModel):
    id: str
    name: str
    description: str
    requires_key: bool

class DataSourceProcessingResponse(BaseModel):
    status: str
    metadata: Dict
    message: str

class DataSourceRequest(BaseModel):
    source: str
    api_key: Optional[str] = None

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