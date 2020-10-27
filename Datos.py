#from typing import final
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,MetaData
from sqlalchemy.orm import relationship,backref
#from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.schema import Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base= declarative_base()

engine= create_engine('sqlite:///datos.db', echo=True)
Base.metadata.create_all(engine)

engine = create_engine('sqlite:///:memory:')
Base.metadata.bind = engine
db_session = sessionmaker()
db_session.bind = engine
session = db_session()

class Alumno(Base):
    __tablename__='alumnos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(Integer,nullable=False) #id login
    #username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    clases = relationship('Clases', secondary='AlumnoClase', backref='alumnos')

    def __repr__(self):
        return f'User {self.name} {self.surname}'
        

class Materia(Base):
    __tablename__ = 'materias'
    idMateria = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    añoCursado = Column(String)
    profesor = Column(String)
    email_profesor = Column(String)
    tipoMateria = Column(String) #si es electiva o no


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
    idComision = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(String)
    cicloLectivo = Column(Integer, nullable=False)
    
    def __init__(self,descripcion,cicloLectivo):
        self.descripcion = descripcion
        self.cicloLectivo = cicloLectivo

    def __repr__(self):
        pass

class Clase(Base):
    __tablename__ = 'clases'
    idClase=Column(Integer,PrimaryKey=True,autoincrement=True,nullable=False)
    
    comision_id = Column(Integer, ForeignKey('comisiones.idComision'), primary_key=True)
   
    materia_id = Column(Integer, ForeignKey('materias.idMateria'), primary_key=True)

    horarioTeoria = Column(String, nullable=False)
    diaTeoria = Column(String, nullable=False)
    aulaTeoria = Column(String, nullable=False)
    horarioPractica = Column(String, nullable=True)
    diaPractica = Column(String, nullable=True)
    aulaPractica = Column(String, nullable=True)

    alumnos = relationship('Alumnos', secondary='AlumnoClase', backref='clases')

    def __init__(self,com_id,mat_id,horaT,diaT,aulaT,horaP,diaP,aulaP):
        self.comision_id = com_id
        self.materia_id = mat_id
        self.horarioTeoria = horaT
        self.diaTeoria = diaT
        self.aulaTeoria = aulaT
        self.horarioPractica = horaP
        self.diaPractica = diaP
        self.aulaPractica = aulaP

    def __repr__(self):
        return f'Clase {self.comision_id}{self.materia_id} Teoria {self.diaTeoria} {self.horarioTeoria} Practica {self.diaPractica}{self.horarioPractica}'


relacion_alumno_clase = Table('AlumnoClase',
    Column('idRelacion',Integer,primary_key=True),
    Column('alumnoId',Integer,ForeignKey('alumnos.id')),
    Column('claseId',Integer,ForeignKey('clases.idClase'))
    )





# class Modulo(Base):
#     __tablename__ = 'modulos'
#     #dias y horarios en los que se cursa, en determinada aula
#     idModulo = Column(Integer, primary_key=True, nullable=False)
#     definicionModulo=Column(String)
#     horarioInicio = Column(Time, nullable=False)
#     horarioFin = Column(Time, nullable=False)
#     dia = Column(Date, nullable=False)
#     aula = Column(String, nullable=False)

#     def __init__(self,horaIni,horaFin,dia,aula,defMod):
#         self.horarioInicio = horaIni
#         self.horarioFin = horaFin
#         self.dia=dia
#         self.aula=aula
#         self.definicionModulo=defMod

#     def __repr__(self):
#         return f'Modulo: {self.idModulo} horarios: {self.horarioInicio} {self.horarioFin} dia: {self.dia} aula: {self.aula} def:{self.definicionModulo}'

# assosiation_table_materia_comision = Table('assosiation_materia_comision',Base.metadata,
#     Column('materias_id',Integer,ForeignKey('materias.idMaterias')),
#     Column('comisiones_id',Integer,ForeignKey('right.id'))
#     )

# '''Falta clase alumno materia'''