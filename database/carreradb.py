from sqlalchemy import Column,Integer,String,null
#from sqlalchemy.orm import relationship

from base import Base

class Carrera(Base):
    __tablename__ = 'carreras'
    idCarrera = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(String)
    cicloLectivo = Column(Integer)
    idInstitucion = Column(Integer, nullable= null)
    #foranea a intitucion, muchos(0,*) a muchos (0,*)

    def __init__(self,descripcion,cicloLectivo):
        self.descripcion=descripcion
        self.cicloLectivo=cicloLectivo