#from typing import final
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
# https://docs.sqlalchemy.org/en/13/index.html
#https://www.fullstackpython.com/sqlalchemy-code-examples.html
#https://docs.sqlalchemy.org/en/14/orm/tutorial.html


class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(INTEGER, nullable=False)  # id login
    password = Column(String, nullable=False)

    # clases = relationship('Comision', secondary='alumnocomisionmateria', backref='alumnos')#problema
    # comision = relationship('Materia', secondary='alumnocomisionmateria', backref='alumnos')#problema

    # def __repr__(self):
    #     return f'User {self.name} {self.surname}'

    def validarUsuario(self, leg, psw):
        #try:
            conn = crearConexion()
            val = conn.query(Alumno).filter(
                Alumno.legajo == leg and Alumno.password == psw).first() #o fetchall()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     val = None
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return val

    def altaUsusario(self, entrada):
        #try:
            conn = crearConexion()
            conn.add(entrada)
            conn.commit()
            q = conn.query(Alumno).filter(Alumno.id == entrada.id).first()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return q


class Materia(Base):
    __tablename__ = 'materias'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    anioCursado = Column(String)
    profesor = Column(String)
    email_profesor = Column(String)
    tipoMateria = Column(String)  # si es electiva o no

    # poner una columna que haga referencia a la tabla (FK)
    # poner la relationship entre las dos tablas

    #comision= relationship('Comision',secondary='comisionmateria')

    # def __init__(self, nombreMateria='inicio', anio='2002', profesor='Pablo gomez', email_profesor='a@gmail.com', tipoMateria='Electiva'):
    #     self.nombreMateria = nombreMateria
    #     self.anioCursado = anio
    #     self.profesor = profesor
    #     self.email_profesor = email_profesor
    #     self.tipoMateria = tipoMateria

    def __repr__(self):
        return f'materia {self.nombreMateria}'

    def traerMaterias(self):
        #try:
            conn = crearConexion()
            q = conn.query(Materia).all()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return q


class Comision(Base):
    __tablename__ = 'comisiones'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nroComision = Column(String)
    cicloLectivo = Column(INTEGER)

    # materia=relationship('Materia',secondary='comisionmateria')

    # def __init__(self, nrocom, cicloLectivo):
    #     self.nroComision = nrocom
    #     self.cicloLectivo = cicloLectivo

    def __repr__(self):
        pass


class ComisionMateria(Base):
    __tablename__ = 'comisionmateria'
    comision_materia_id = Column(Integer, primary_key=True)
    horarioTeoria = Column(String, nullable=False)
    diaTeoria = Column(String, nullable=False)
    aulaTeoria = Column(String, nullable=False)
    horarioPractica = Column(String, nullable=True)
    diaPractica = Column(String, nullable=True)
    aulaPractica = Column(String, nullable=True)

    materia_id = Column(Integer, ForeignKey(Materia.id))
    comision_id = Column(Integer, ForeignKey(Comision.id))

    relMateria = relationship("Materia", backref="materias", foreign_keys=[materia_id])
    relComision = relationship("Comision", backref="comisiones", foreign_keys=[comision_id])

    # alumnos = relationship('Alumno', secondary='alumnocomisionmateria', back_populates='comisionmateria')

    # def __init__(self, horaT='7:00-9:00', diaT='Lunes', aulaT='404', horaP='9:00-11:00', diaP='Martes', aulaP='505'):
    #     self.horarioTeoria = horaT
    #     self.diaTeoria = diaT
    #     self.aulaTeoria = aulaT
    #     self.horarioPractica = horaP
    #     self.diaPractica = diaP
    #     self.aulaPractica = aulaP

    # def __repr__(self):
    #     return f'Clase {self.comision_id}{self.materia_id} Teoria {self.diaTeoria} {self.horarioTeoria} Practica {self.diaPractica}{self.horarioPractica}'

    def infoMat(self, cm):
        #try:
            conn = crearConexion()
            nm = conn.query(ComisionMateria.materia.nombreMateria).filter(
                ComisionMateria.materia_id == cm.materia_id).first()
            nc = conn.query(ComisionMateria.comision.nroComision).filter(
                ComisionMateria.comision_id == cm.comision_id).first()
        # except SQLAlchemyError as e:et
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return nm, nc

    def traerComisiones(self, m):
        #try:
            conn = crearConexion()
            q = conn.query(Comision).filter(ComisionMateria.materia_id == m.id and ComisionMateria.comision_id == Comision.id).all()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return q

    def devolver(self, m, c):
        #try:
            conn = crearConexion()
            q = conn.query(ComisionMateria).filter(ComisionMateria.materia_id == m.id and ComisionMateria.comision_id == Comision.id).first()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return q


class AlumnoComisionMateria(Base):  # clase
    __tablename__ = 'alumnocomisionmateria'
    #id = Column(Integer, primary_key=True)

    alumno_id = Column(Integer, ForeignKey('alumnos.id'), primary_key=True)
    comision_materia_id = Column(Integer, ForeignKey(
        'comisionmateria.comision_materia_id'), primary_key=True)

    relAlumno = relationship(
        "Alumno", backref="alumnos", foreign_keys=[alumno_id])
    relComisionMateria = relationship(
        "ComisionMateria", backref="comisionmateria", foreign_keys=[comision_materia_id])

    def __repr__(self):
        pass

    def alta(self, entrada):
        #try:
            conn = crearConexion()
            conn.add(entrada)
            conn.commit()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return True

    def traerMateriasAlumno(self, alu):
        # try:
            conn = crearConexion()
            q = conn.query(Materia.nombreMateria).filter(
                AlumnoComisionMateria.alumno_id == alu.id and 
                AlumnoComisionMateria.comision_materia_id == ComisionMateria.comision_materia_id and
                ComisionMateria.materia_id == Materia.id).all()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return q

    def bajaMateria(self, a, cm):
        #try:
            conn = crearConexion()
            conn.query(AlumnoComisionMateria).filter(AlumnoComisionMateria.alumno.id == a.id 
            and AlumnoComisionMateria.comisionMateria.comision_materia_id == cm.comision_materia_id).delete()
            conn.commit()
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     print(error)
        # finally:
            cerrarConexion(conn)
            return True


def crearConexion():
    engine = create_engine('sqlite:///datos.db', echo=True)
    Base.metadata.bind = engine
    db_session = sessionmaker()
    db_session.bind = engine
    session = db_session()
    return session


def crearTablas():
    engine = create_engine('sqlite:///datos.db')
    meta = MetaData()
    # Base=declarative_base()
    meta.create_all(engine)


def cerrarConexion(sess):
    error = 'Session Cerrada'
    try:
        sess.close()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
    finally:
        return error
