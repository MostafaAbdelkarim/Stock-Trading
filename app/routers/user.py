from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"Message": "Successful"}


@router.put("/deposite", status_code=status.HTTP_200_OK)
def deposite_money_to_user(user: schemas.UserTransaction, db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.id == user.user_id)
    if query_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {user.user_id} is not found")
    new_user: schemas.UserBase = query_user.first()
    new_user.amount += user.amount
    query_user.update({"amount": new_user.amount}, synchronize_session=False)
    db.commit()
    return {"Success": f"Deposited: {user.amount} to User: {new_user.first_name}"}


@router.put("/withdraw", status_code=status.HTTP_200_OK)
def withdraw_money_from_user(user: schemas.UserTransaction, db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.id == user.user_id)
    if query_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {user.user_id} is not found")
    new_user: schemas.UserBase = query_user.first()
    new_user.amount -= user.amount
    query_user.update({"amount": new_user.amount}, synchronize_session=False)
    db.commit()
    return {"Success": f"Withdrawn: {user.amount} from User: {new_user.first_name}"}


@router.post("/user", status_code=status.HTTP_200_OK)
def get_user_by_id(user: schemas.UserIn, db: Session = Depends(get_db)):
    query = db.query(models.User).options(joinedload(
        models.User.stocks)).filter(models.User.id == user.user_id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user.user_id} is not found")

    return {"User": query.all()}
