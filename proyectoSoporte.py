from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()

class User(Base):
    __tablename__:'user'
    
        
