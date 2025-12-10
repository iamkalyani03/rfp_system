import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Load `.env`
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL missing. Add to .env")

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from .models import RFP, Vendor, Proposal
    SQLModel.metadata.create_all(engine)
