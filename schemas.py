from pydantic import BaseModel
from datetime import datetime


class SummaryCreate(BaseModel):
    text: str

class SummaryOut(BaseModel):
    id: int
    original_text: str
    summarized_text: str
    created_at: datetime

    class Config:
        orm_mode = True