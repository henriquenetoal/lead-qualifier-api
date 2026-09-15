from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/leads", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.get("/leads", response_model=list[schemas.LeadResponse])
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return leads

@app.patch("/leads/{lead_id}", response_model=schemas.LeadResponse)
def update_lead_status(lead_id: int, status: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = status
    db.commit()
    db.refresh(lead)
    return lead