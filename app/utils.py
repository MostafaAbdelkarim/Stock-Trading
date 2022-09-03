from sqlalchemy.orm import Session
from . import models
from .models import Stock, User
from .database import get_engine


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def initial_data_seeder():
    get_or_update_users()
    get_or_update_stocks()


def get_or_update_users():
    db: Session = Session(get_engine())
    query = db.query(models.User).filter(models.User.first_name == 'Mostafa')
    if not query.first():
        user_1 = User(
            first_name='Mostafa',
            last_name='ElDahshan',
            email='mostafa@gmail.com',
            password='123345678',
            amount=200)
        db.add(user_1)
        db.commit()

    query = db.query(models.User).filter(models.User.first_name == 'Ahmed')
    if not query.first():
        user_2 = User(
            first_name='Ahmed',
            last_name='ElDahshan',
            email='ahmed@gmail.com',
            password='123345678',
            amount=100)
        db.add(user_2)
        db.commit()


def get_or_update_stocks():
    db: Session = Session(get_engine())
    query = db.query(models.Stock).filter(models.Stock.name == 'CIB')
    if not query.first():
        cib_stock = Stock(
            name='CIB',
            price=20,
            availability=20
        )
        db.add(cib_stock)
        db.commit()

    query = db.query(models.Stock).filter(models.Stock.name == 'Edita')
    if not query.first():
        edita_stock = Stock(
            name='Edita',
            price=120,
            availability=50
        )
        db.add(edita_stock)
        db.commit()

    query = db.query(models.Stock).filter(models.Stock.name == 'Hamada Inc')
    if not query.first():
        hamada_stock = Stock(
            name='Hamada Inc',
            price=150,
            availability=20
        )
        db.add(hamada_stock)
        db.commit()
