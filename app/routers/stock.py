from configparser import RawConfigParser
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix="/api/v1/stocks",
    tags=['Stocks']
)


@router.get("/{stock_name}", status_code=status.HTTP_200_OK, response_model=schemas.StockPriceOut)
def get_current_stock_price(stock_name: str, db: Session = Depends(get_db)):
    stock_query = db.query(models.Stock).filter(
        models.Stock.name == stock_name)
    if stock_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Stock with name: {stock_name} is not found")
    return stock_query.first()


@router.post("/buy", status_code=status.HTTP_200_OK)
def user_buy_stocks(user: schemas.UserStockTransactions, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user.user_id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user.user_id} is not found")
    stock_query = db.query(models.Stock).filter(
        models.Stock.stock_id == user.stock_id)
    if not stock_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Stock with id: {user.stock_id} is not found")
    found_user: schemas.UserBase = user_query.first()
    found_stock: schemas.StockBase = stock_query.first()
    if (found_stock.availability <= 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Stock not available for purchase")
    if found_user.amount < found_stock.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User cannot afford this stock")
    # change price condition later
    num_of_stocks = (user.total / found_stock.price)
    if (user.lower_bound < found_stock.price and user.upper_bound > found_stock.price):
        junction_query = db.query(models.UserStock).filter(
            models.UserStock.user_id == user.user_id).filter(models.UserStock.stock_id == user.stock_id)
        found_user.amount -= user.total
        if (not isinstance(num_of_stocks, int)):
            num_of_stocks = utils.truncate(num_of_stocks)
        if (found_user.amount <= 0):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"No available funds to buy with given total")
        if junction_query.first():
            data: schemas.UserStockBase = junction_query.first()
            junction_query.update(
                {'quantity': data.quantity + num_of_stocks}, synchronize_session=False)
            db.commit()
        else:
            junction_add = models.UserStock(
                user_id=user.user_id, stock_id=user.stock_id, quantity=num_of_stocks)
            db.add(junction_add)
            db.commit()
        user_query.update({'amount': found_user.amount},
                          synchronize_session=False)
        db.commit()
        return {"Success": f"User: {found_user.first_name} bought {num_of_stocks} of Stock {found_stock.name} "}
    else:
        return {"Fail": f"Upper/Lower bounds does not match.. please retry"}


@router.post("/sell", status_code=status.HTTP_200_OK)
def get_stock_by_id(user: schemas.UserStockTransactions, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user.user_id)
    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    stock_query = db.query(models.Stock).filter(
        models.Stock.stock_id == user.stock_id)
    if not stock_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock not found")
    user_stock_query = db.query(models.UserStock).filter(
        models.UserStock.user_id == user.user_id).filter(models.UserStock.stock_id == user.stock_id)
    if user_stock_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User does not have this stock to sell")
    user_found: schemas.UserBase = user_query.first()
    stock_found: schemas.StockBase = stock_query.first()
    if (user.total < stock_found.price):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Stock price is higher than total")
    num_of_stocks = (user.total / stock_found.price)
    if (not isinstance(num_of_stocks, int)):
        num_of_stocks = utils.truncate(num_of_stocks)
    if (user.lower_bound < stock_found.price and user.upper_bound > stock_found.price):
        user_found.amount += user.total
        data: schemas.UserStockBase = user_stock_query.first()
        if (data.quantity - num_of_stocks <= 0):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"No available stocks with given total")
        user_stock_query.update(
            {'quantity': data.quantity - num_of_stocks}, synchronize_session=False)
        user_query.update({'amount': user_found.amount},
                          synchronize_session=False)
        db.commit()
        return {"Success": f"User {user_found.first_name} Sold {num_of_stocks} of Stock {stock_found.name}"}
    return {"Fail": "Upper/Lower bound does not meet"}


@router.get("/stock/{id}", status_code=status.HTTP_200_OK)
def get_stock_by_id(id: str, db: Session = Depends(get_db)):
    query = db.query(models.Stock).options(joinedload(
        models.Stock.users)).filter(models.Stock.stock_id == id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Stock with id: {id} is not found")
    return {"Stock": query.all()}
