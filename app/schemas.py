from pydantic import BaseModel
from datetime import datetime


class CampaignCreate(BaseModel):
    name: str


class CampaignResponse(BaseModel):
    code: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
