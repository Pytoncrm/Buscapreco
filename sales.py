from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/sales", tags=["sales"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    new_sale = models.Sale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale
