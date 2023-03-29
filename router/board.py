from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.member import Member, MemberCreate, MemberUpdate, MemberOut
from config.db import session

router = APIRouter()


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()


@router.post("/boards", response_model=MemberOut)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/boards/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/boards/{member_id}", response_model=MemberOut)
def update_member(member_id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    update_data = member.dict(exclude_unset=True)
    for var, value in update_data.items():
        setattr(db_member, var, value)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/boards/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted successfully"}
