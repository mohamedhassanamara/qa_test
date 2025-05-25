from fastapi import FastAPI, Depends
from openai import OpenAI
import database, models, schemas
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/Summirze/{text}")
def summarize_text(text:str, db: Session = Depends(get_db)):
    model = "qanswer-llm"
    client = OpenAI(
        base_url="https://dev.qanswer.ai/llm",
        api_key=openai_api_key,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": f"Summarize this: {text} in 1 sentence."},
        ]
    )

    summary = models.Summary(
        original_text=text,
        summarized_text=response.choices[0].message.content.strip(),
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary.summarized_text


@app.get("/summaries/", response_model=list[schemas.SummaryOut])
def get_summaries(db: Session = Depends(get_db)):
    return db.query(models.Summary).order_by(models.Summary.created_at.desc()).all()
