import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, MetaData, and_, create_engine
from sqlalchemy import engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime, INTEGER

Base = declarative_base()
engine=create_engine('sqlite:///datos.db',echo=True)

class Comision(Base):
    __tablename__ = 'comisiones'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nroComision = Column(String)
    cicloLectivo = Column(INTEGER)

class Materia(Base):
    __tablename__ = 'materias'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    anioCursado = Column(String)
    tipoMateria = Column(String)

class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(String, nullable=False)  # id login
    password = Column(String, nullable=False)

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



#Borrar tablas
Base.metadata.drop_all(engine)

#Crear tablas
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.add_all([
Alumno(nombre='Manuel',apellido='Lopez',email='manu@gmail.com',legajo='42846',password='123456'),
Alumno(nombre='Mauro',apellido='Lamagni',email='mauro@gmail.com',legajo='55555',password='555555'),
Alumno(nombre='Rocio',apellido='Salinas',email='ro@gmail.com',legajo='44444',password='4444444'),
Comision(nroComision=101,cicloLectivo='2020'),
Comision(nroComision=102,cicloLectivo='2020'),
Comision(nroComision=103,cicloLectivo='2020'),
Materia(nombreMateria='Matematica',anioCursado='1',tipoMateria=''),
Materia(nombreMateria='Algebra',anioCursado='1',tipoMateria=''),
Materia(nombreMateria='Fisica',anioCursado='2',tipoMateria=''),
Materia(nombreMateria='Recursos Humanos',anioCursado='3',tipoMateria='Optativa'),
ComisionMateria(horarioTeoria = '10:30' ,
    diaTeoria = 'Lunes',
    aulaTeoria = '101',
    horarioPractica = '10:30',
    diaPractica = 'Jueves',
    aulaPractica = '101',
    profesorT = 'Mario',
    email_profesorT = 'mario@gmail.com',
    profesorP= 'Juan',
    email_profesorP= 'juan@gmail.com',
    materia_id =1 ,
    comision_id = 1),
ComisionMateria(horarioTeoria = '7:00' ,
    diaTeoria = 'Martes',
    aulaTeoria = '107',
    horarioPractica = '12:00',
    diaPractica = 'Viernes',
    aulaPractica = '108',
    profesorT = 'Pablo',
    email_profesorT = 'pablo@gmail.com',
    profesorP= 'Maria',
    email_profesorP= 'maria@gmail.com',
    materia_id =4 ,
    comision_id = 3),
AlumnoComisionMateria(alumno_id=1 ,comision_materia_id=1)
    ])

session.commit()
