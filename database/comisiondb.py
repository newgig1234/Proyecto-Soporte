from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship, backref
#from sqlalchemy.orm import relationship

from base import Base

class Comision(Base):
    #cambiar en md
    __tablename__ = 'comisiones'
    idComision = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(String)
    cicloLectivo = Column(Integer, nullable=False)
    materias = relationship('Materia', secondary='clases')

    def __init__(self,descripcion,cicloLectivo):
        self.descripcion=descripcion
        self.cicloLectivo=cicloLectivo

class Clase(Base):
    __tablename__ = 'clases'
    comision_id = Column(Integer, ForeignKey('comisiones.idComision'), primary_key=True)
    materia_id = Column(Integer, ForeignKey('materias.idMateria'), primary_key=True)

    alumnos = relationship('Alumnos', secondary='alumnos_clases')
