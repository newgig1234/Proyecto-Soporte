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


engine = create_engine('sqlite:///C:\\Users\\manolo\\Desktop\\Proyecto_Soporte\\Proyecto-Soporte\\datos.db')
meta = MetaData()

alumnos = Table('Alumnos',meta,
    Column('id',Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('nombre',String),
    Column('apellido',String),
    Column('email',String),
    Column('legajo',Integer),
    Column('password',String)
)

materias = Table('Materias',meta,
    Column('id',Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('nombre',String),
    Column('año_cursado',String),
    Column('profesor',String),
    Column('email_profesor',String),
    Column('tipo_materia',Integer)
)

comision = Table ('Comision', meta,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('descripcion',String),
    Column('cicloLectivo',String)
)

clase = Table ('Clase', meta,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('horarioTeoria',String),
    Column('diaTeoria',String),
    Column('aulaTeoria',String),
    Column('horarioPractica',String),
    Column('diaPractica',String),
    Column('aulaPractica',String)
)
    
    # comision_id = Column(Integer, ForeignKey('comisiones.idComision'), primary_key=True)
    # materia_id = Column(Integer, ForeignKey('materias.idMateria'), primary_key=True)

meta.create_all(engine)