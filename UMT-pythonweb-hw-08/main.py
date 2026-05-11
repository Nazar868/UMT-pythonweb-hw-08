from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import models
import crud
import schemas

from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")


@app.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    return crud.create_contact(db, contact)


@app.get("/contacts/", response_model=list[schemas.ContactResponse])
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(
    contact_id: int,
    updated_contact: schemas.ContactUpdate,
    db: Session = Depends(get_db)
):
    contact = crud.update_contact(db, contact_id, updated_contact)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.delete_contact(db, contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted"}


@app.get("/search/", response_model=list[schemas.ContactResponse])
def search_contacts(
    query: str = Query(...),
    db: Session = Depends(get_db)
):
    return crud.search_contacts(db, query)


@app.get("/birthdays/", response_model=list[schemas.ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db)
