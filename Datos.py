#from typing import final
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,MetaData
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy.sql.sqltypes import  DateTime, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Alumno(Base):
    __tablename__='alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(INTEGER,nullable=False) #id login
    password = Column(String, nullable=False)

    clases = relationship('Comision', secondary='alumnocomisionmateria', backref='alumnos')#problema
    comision = relationship('Materia', secondary='alumnocomisionmateria', backref='alumnos')#problema


    def __repr__(self):
        return f'User {self.name} {self.surname}'

    def validarUsuario(self,leg,psw):
        val=None
        try:
            conn = crearConexion()
            val = conn.query(Alumno).filter(Alumno.legajo == leg and Alumno.password == psw).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            val= None
            print(error)
        finally:
            cerrarConexion(conn)
            return val
    
    def altaUsusario(self,entrada):
        conn =None
        try:
            conn = crearConexion()
            conn.add(entrada)
            conn.commit()
            q = conn.query(Alumno).filter(Alumno.id == entrada.id).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error) 
        finally:
            cerrarConexion(conn)
            return q

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

    def traerMaterias(self):
        q=None
        try:
            conn = crearConexion()
            q = conn.query(Materia).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return q

class Comision(Base):
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
    
    alumno=relationship('Alumno',back_populates='alumnos')
    comisionMateria=relationship('ComisionMaterias',back_populates='comisionmateria')

    alumnos = relationship('Materia', secondary='comisionmateria', backref='alumnocomisionmateria')
    alumnos = relationship('Comision', secondary='comisionmateria', backref='alumnocomisionmateria')

    def __repr__(self):
        pass


    def alta(self,entrada):
        try:
            conn = crearConexion()
            conn.add(entrada)
            conn.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error) 
        finally:
            cerrarConexion(conn)
            return True

    def traerMateriasAlumno(self,alu):
        q=None
        try:
            conn = crearConexion()
            q = conn.query(AlumnoComisionMateria.comisionMateria).filter(AlumnoComisionMateria.alumno.id == alu.id).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return q
    
    def bajaMateria(self,a,cm):
        try:
            conn = crearConexion()
            conn.query(AlumnoComisionMateria).filter(AlumnoComisionMateria.alumno.id == a.id and AlumnoComisionMateria.comisionMateria.comision_materia_id == cm.comision_materia_id).delete()
            conn.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return True


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

    comision=relationship('Materia',back_populates='comision')
    materia=relationship('Comision',back_populates='materias')

    alumnos = relationship('Alumno', secondary='alumnocomisionmateria', back_populates='comisionmateria')


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
        nm=nc=None
        try:
            conn = crearConexion()
            nm = conn.query(ComisionMateria.materia.nombreMateria).filter(ComisionMateria.materia_id == cm.materia_id).fetchone()
            nc = conn.query(ComisionMateria.comision.descripcion).filter(ComisionMateria.comision_id == cm.comision_id).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return nm,nc
    
    def traerComisiones(self,m):
        q=None
        try:
            conn = crearConexion()
            q = conn.query(Comision).filter(ComisionMateria.materia_id==m.id and ComisionMateria.comision_id == Comision.id).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return q
    
    def devolver(self,m,c):
        q=None
        try:
            conn = crearConexion()
            q = conn.query(ComisionMateria).filter(ComisionMateria.materia_id==m.id and ComisionMateria.comision_id == Comision.id).fetchone()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
        finally:
            cerrarConexion(conn)
            return q


def crearConexion():
    engine=create_engine('sqlite:///datos.db', echo=True)
    Base.metadata.bind=engine
    db_session=sessionmaker()
    db_session.bind=engine
    session=db_session()
    return session

def crearTablas():
    engine=create_engine('sqlite:///datos.db')
    meta=MetaData()
    #Base=declarative_base()
    meta.create_all(engine)

def cerrarConexion(sess):
    error='Session Cerrada'
    try:
        sess.close()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
    finally:
        return error

