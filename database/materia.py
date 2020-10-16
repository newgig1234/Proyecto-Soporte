from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.orm import relationship

from base import Base

class Materia(Base):
    __tablename__ = 'materias'
    idMateria = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcionMateria = Column(String)

    comisiones = relationship('Comisiones', secondary='clases')




    def __init__(self,descripcionMateria):
        self.descripcionMateria=descripcionMateria