# backend/app/schemas.py
from pydantic import BaseModel
from typing import List

class RFPCreate(BaseModel):
    text: str

class VendorCreate(BaseModel):
    name: str
    email: str

class SendRFPBody(BaseModel):
    vendor_ids: List[int]
    rfp_id: int
