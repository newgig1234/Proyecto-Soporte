from sqlalchemy import Column,String,Integer
#from sqlalchemy.orm import relationship

from base import Base

class Aula(Base):
    __tablename__ = 'aulas'
    idAula = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(String)
    piso = Column(String)
    mapa = Column() #Tipo foto
    #mapa= foto(ver si se puede) del piso y la X marca donde esta el teso... aula.

    def __init__(self,descripcion,piso,mapa):
        self.descripcion = descripcion
        self.piso = piso
        self.mapa = mapa