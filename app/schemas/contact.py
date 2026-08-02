from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ContactBase(BaseModel):
    company_name : str
    inn : str
    kpp : str
    phone : str

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    company_name: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None
    phone : Optional[str] = None

class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id : int
    created_at : datetime
    updated_at : Optional[datetime] = None

