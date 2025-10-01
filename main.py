# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import random
import string

from app.services import SearchService
from app.schemas import CampaignResponse, CampaignCreate

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Monster Manual API")


def generate_campaign_code():
    prefix = random.choice(prefixes)
    numbers = "".join(random.choices(string.digits, k=2))
    return f"{prefix}{numbers}"


@app.get("/")
def read_root():
    return {"message": "Monster Manual API"}


@app.get("/api/search")
def search_entries(q: str, limit: int = 10):
    results = SearchService.search_entries(q, limit)
    return {"query": q, "results": results}


@app.post("/api/campaign/create", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):

    code = generate_campaign_code()
    while db.query(models.Campaign).filter(models.Campaign.code == code).first():
        code = generate_campaign_code()

    db_campaign = models.Campaign(code=code, name=campaign.name)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)

    return db_campaign


@app.get("/api/campaign/{code}", response_model=CampaignResponse)
def get_campaign(code: str, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.code == code).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
