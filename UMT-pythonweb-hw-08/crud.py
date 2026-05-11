from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Contact
from schemas import ContactCreate
from datetime import date, timedelta


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    return db_contact


def get_contacts(db: Session):
    return db.query(Contact).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = get_contact(db, contact_id)

    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)

        db.commit()
        db.refresh(db_contact)

    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)

    if db_contact:
        db.delete(db_contact)
        db.commit()

    return db_contact


def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()


def upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).all()

    result = []

    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)

        if today <= birthday_this_year <= next_week:
            result.append(contact)

    return result
