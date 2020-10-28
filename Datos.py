#from typing import final
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,MetaData
from sqlalchemy.orm import backref, relationship
#from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.sqltypes import Boolean, DateTime, INTEGER
from sqlalchemy.sql.schema import Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

engine= create_engine('sqlite:///datos.db', echo=True)
Base = declarative_base()



class Alumno(Base):
    __tablename__='alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(INTEGER,nullable=False) #id login
    #username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    clases = relationship('Clases', secondary='AlumnoClase', backref='alumnos')

    def __repr__(self):
        return f'User {self.name} {self.surname}'
        

class Materia(Base):
    __tablename__ = 'materias'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    añoCursado = Column(String)
    profesor = Column(String)
    email_profesor = Column(String)
    tipoMateria = Column(String) #si es electiva o no

    comision= relationship('Comision',secondary='alumnoclase')

    def __init__(self,nombreMateria,año,profesor,email_profesor,tipoMateria):
        self.nombreMateria = nombreMateria
        self.añoCursado = año
        self.profesor = profesor
        self.email_profesor = email_profesor
        self.tipoMateria = tipoMateria

    def __repr__(self):
        return f'materia {self.nombreMateria}'

    def agregarMateria(self):
        pass

    def buscarMateria(self):#buscar als materias para hacer el popup
        pass


class Comision(Base):
    #cambiar en md
    __tablename__ = 'comisiones'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(String)
    cicloLectivo = Column(INTEGER)
    numeroComision=Column(INTEGER)

    materia=relationship('Materia',secondary='alumnoclase')
    
    def __init__(self,descripcion,cicloLectivo):
        self.descripcion = descripcion
        self.cicloLectivo = cicloLectivo

    def __repr__(self):
        pass

class AlumnoComisionMateria(Base):
    __tablename__='alumnocomisionmateria'
    alumno_id=Column(INTEGER,ForeignKey('alumnos.id'),primary_key=True)
    comision_materia_id=Column(INTEGER,ForeignKey('comisionmateria.comision_materia_id'),primary_key=True)
    
    def __repr__(self):
        pass

class ComisionMateria(Base):
    __tablename__='comisionmateria'
    comision_materia_id=Column(Integer,primary_key=True)
    comision_id=Column(INTEGER,ForeignKey('comisiones.id'),primary_key=True)
    materia_id=Column(INTEGER,ForeignKey('materias.id'),primary_key=True)
    #extra data
    horarioTeoria = Column(String, nullable=False)
    diaTeoria = Column(String, nullable=False)
    aulaTeoria = Column(String, nullable=False)
    horarioPractica = Column(String, nullable=True)
    diaPractica = Column(String, nullable=True)
    aulaPractica = Column(String, nullable=True)
    fechaInscripcion=Column(DateTime)

    comision=relationship('Materia',back_populates='comisiones')
    materia=relationship('Comision',back_populates='materias')



    def __init__(self,horaT='7:00-9:00',diaT='Lunes',aulaT='404',horaP='9:00-11:00',diaP='Martes',aulaP='505'):
        self.horarioTeoria = horaT
        self.diaTeoria = diaT
        self.aulaTeoria = aulaT
        self.horarioPractica = horaP
        self.diaPractica = diaP
        self.aulaPractica = aulaP

    def __repr__(self):
        return f'Clase {self.comision_id}{self.materia_id} Teoria {self.diaTeoria} {self.horarioTeoria} Practica {self.diaPractica}{self.horarioPractica}'


Base.metadata.create_all(engine)
