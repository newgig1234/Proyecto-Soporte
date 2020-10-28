#from typing import final
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,MetaData
from sqlalchemy.orm import backref, relationship, sessionmaker
#from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.sqltypes import Boolean, DateTime, INTEGER
from sqlalchemy.sql.schema import Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.exc import SQLAlchemyError

engine= create_engine('sqlite:///datos.db', echo=True)
Base = declarative_base()
Session=sessionmaker(bind=engine)
db=scoped_session(Session)

class Alumno(Base):
    __tablename__='alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(INTEGER,nullable=False) #id login
    #username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    clases = relationship('Clases', secondary='alumnocomisionmateria', backref='alumnos')

    def __repr__(self):
        return f'User {self.name} {self.surname}'

    def validarUsuario(self,leg,psw):
        val=None
        try:
            conn = engine.connect()
            val = self.db.query(Alumno).filter(Alumno.legajo == leg and Alumno.password == psw).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            val= None
            print(error)
        finally:
            conn.close()
            return val
    
    def altaUsusario(self,entrada):
        # self.legajo = leg
        # self.nombre = nom
        # self.apellido = app
        # self.email = mail
        # self.password = psw
        try:
            conn = engine.connect()
            self.session.add(entrada)
            self.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error) 
        finally:
            conn.close()

class Materia(Base):
    __tablename__ = 'materias'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    añoCursado = Column(String)
    profesor = Column(String)
    email_profesor = Column(String)
    tipoMateria = Column(String) #si es electiva o no

    comision= relationship('Comision',secondary='comisionmateria')

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

    materia=relationship('Materia',secondary='comisionmateria')
    
    def __init__(self,descripcion,cicloLectivo):
        self.descripcion = descripcion
        self.cicloLectivo = cicloLectivo

    def __repr__(self):
        pass


class AlumnoComisionMateria(Base):
    __tablename__='alumnocomisionmateria'
    alumno_id=Column(INTEGER,ForeignKey('alumnos.id'),primary_key=True)
    comision_materia_id=Column(INTEGER,ForeignKey('comisionmateria.comision_materia_id'),primary_key=True)
    
    alumno=relationship('Alumnos',back_populates='alumnos')
    comisionMateria=relationship('ComisionMaterias',back_populates='comisionmateria')

    def __repr__(self):
        pass

    def traerMateriasAlumno(self,alu):
        try:
            conn = engine.connect()
            q = self.session.query(AlumnoComisionMateria.comisionMateria).filter(AlumnoComisionMateria.alumno.id == alu.id).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            conn.close()
            return q


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

    alumnos = relationship('Alumnos', secondary='alumnocomisionmateria', backref='comisionmateria')


    def __init__(self,horaT='7:00-9:00',diaT='Lunes',aulaT='404',horaP='9:00-11:00',diaP='Martes',aulaP='505'):
        self.horarioTeoria = horaT
        self.diaTeoria = diaT
        self.aulaTeoria = aulaT
        self.horarioPractica = horaP
        self.diaPractica = diaP
        self.aulaPractica = aulaP

    def __repr__(self):
        return f'Clase {self.comision_id}{self.materia_id} Teoria {self.diaTeoria} {self.horarioTeoria} Practica {self.diaPractica}{self.horarioPractica}'

    def infoMat(self,cm):
        try:
            conn = engine.connect()
            nm = self.session.query(ComisionMateria.materia.nombreMateria).filter(ComisionMateria.materia_id == cm.materia_id).fetchone()
            nc = self.session.query(ComisionMateria.comision.descripcion).filter(ComisionMateria.comision_id == cm.comision_id).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            conn.close()
            return nm,nc


Base.metadata.create_all(engine)
