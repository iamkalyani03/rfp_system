# backend/app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class RFP(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    raw_input: str
    structured_json: dict = Field(sa_column=Column(JSON), default={})  # JSON field

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: int
    rfp_id: int
    content_raw: str
    parsed_json: dict = Field(sa_column=Column(JSON), default={})  # JSON field
    score: Optional[float] = None
    recommendation: Optional[str] = None
