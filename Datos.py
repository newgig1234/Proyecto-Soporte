import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, MetaData, and_ , create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
# https://docs.sqlalchemy.org/en/13/index.html
# https://www.fullstackpython.com/sqlalchemy-code-examples.html
# https://docs.sqlalchemy.org/en/14/orm/tutorial.html


class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(String, nullable=False)  # id login
    password = Column(String, nullable=False)


    def validarUsuario(self, leg, psw):
        conn = crearConexion()
        val = conn.query(Alumno).filter(and_(
            Alumno.legajo == leg ,Alumno.password == psw)).first()
        cerrarConexion(conn)
        return val

    def altaUsuario(self,leg,nom,app,mail,cont1):
        conn = crearConexion()
        conn.add(Alumno(legajo=leg,nombre=nom,apellido=app,email=mail,password=cont1))
        conn.commit()
        cerrarConexion(conn)
    
    def buscarUsuario(self,leg):
        conn = crearConexion()
        q = conn.query(Alumno).filter(Alumno.legajo == leg).first()
        cerrarConexion(conn)
        return q


class Materia(Base):
    __tablename__ = 'materias'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    anioCursado = Column(String)
    tipoMateria = Column(String)

    def traerMaterias(self): 
        conn = crearConexion()
        q = conn.query(Materia).all()
        cerrarConexion(conn)
        return q


class Comision(Base):
    __tablename__ = 'comisiones'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nroComision = Column(String)
    cicloLectivo = Column(INTEGER)


class ComisionMateria(Base):
    __tablename__ = 'comisionmateria'
    comision_materia_id = Column(Integer, primary_key=True)
    horarioTeoria = Column(String, nullable=False)
    diaTeoria = Column(String, nullable=False)
    aulaTeoria = Column(String, nullable=False)
    horarioPractica = Column(String, nullable=True)
    diaPractica = Column(String, nullable=True)
    aulaPractica = Column(String, nullable=True)
    profesorT = Column(String)
    email_profesorT = Column(String)
    profesorP= Column(String)
    email_profesorP=Column(String)

    materia_id = Column(Integer, ForeignKey(Materia.id))
    comision_id = Column(Integer, ForeignKey(Comision.id))

    relMateria = relationship("Materia", backref="materias", foreign_keys=[materia_id])
    relComision = relationship("Comision", backref="comisiones", foreign_keys=[comision_id])

    def infoMat(self, cm):
        conn = crearConexion()
        nm = conn.query(ComisionMateria.relMateria.nombreMateria).filter(
            ComisionMateria.materia_id == cm.materia_id).first()
        nc = conn.query(ComisionMateria.relComision.nroComision).filter(
            ComisionMateria.comision_id == cm.comision_id).first()
        cerrarConexion(conn)
        return nm, nc
    

    def traerComisiones(self, m):
        conn = crearConexion()
        q = conn.query(Comision).filter(and_(ComisionMateria.materia_id == m.id, ComisionMateria.comision_id == Comision.id)).all()
        cerrarConexion(conn)
        return q

    def devolver(self, m, c):
        conn = crearConexion()
        q = conn.query(ComisionMateria).filter(and_(ComisionMateria.materia_id == m.id, ComisionMateria.comision_id == c.id)).first()
        cerrarConexion(conn)
        return q
    
    def nombreMat(self):
        conn = crearConexion()
        q = conn.query(Materia).filter(ComisionMateria.materia_id == Materia.id).first()
        cerrarConexion(conn)
        return q


class AlumnoComisionMateria(Base):
    __tablename__ = 'alumnocomisionmateria'

    alumno_id = Column(Integer, ForeignKey('alumnos.id'), primary_key=True)
    comision_materia_id = Column(Integer, ForeignKey(
        'comisionmateria.comision_materia_id'), primary_key=True)

    relAlumno = relationship(
        "Alumno", backref="alumnos", foreign_keys=[alumno_id])
    relComisionMateria = relationship(
        "ComisionMateria", backref="comisionmateria", foreign_keys=[comision_materia_id])

    def __repr__(self):
        pass

    def alta(self,cm,u):
        conn = crearConexion()
        conn.add(AlumnoComisionMateria(alumno_id=u.id,comision_materia_id=cm.comision_materia_id))
        conn.commit()
        cerrarConexion(conn)
        return True

    def traerMateriasAlumno(self, alu):
        conn = crearConexion()
        q = conn.query(ComisionMateria).filter(and_(
            AlumnoComisionMateria.alumno_id == alu.id, 
            AlumnoComisionMateria.comision_materia_id == ComisionMateria.comision_materia_id,)).all()
        cerrarConexion(conn)
        return q

    def bajaMateria(self, a, cm):
        conn = crearConexion()
        conn.query(AlumnoComisionMateria).filter(and_(AlumnoComisionMateria.relAlumno.id == a.id 
            ,AlumnoComisionMateria.relComisionMateria.comision_materia_id == cm.comision_materia_id)).delete()
        conn.commit()
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
