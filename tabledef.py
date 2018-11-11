from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///app.db')
Base = declarative_base()
 
########################################################################
class FoodItem(Base):
    """"""
    __tablename__="food"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    price=Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self,name,price):
        self.name = name
        self.price = price

class MrpFoodItem(Base):
    """"""
    __tablename__="MRPfood"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    #----------------------------------------------------------------------
    def __init__(self,name):
        self.name = name

class BillItem():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,name,unit,price):        
        self.name = name
        self.units = unit
        self.price = float("{0:.2f}".format(float(price)))
        self.total = float(unit)*float(price)
        self.total = float("{0:.2f}".format(self.total))

# create tables
Base.metadata.create_all(engine)
