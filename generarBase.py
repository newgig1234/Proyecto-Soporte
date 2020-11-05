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
Comision(nroComision=101,cicloLectivo='2020'),  #1
Comision(nroComision=102,cicloLectivo='2020'),  #2
Comision(nroComision=201,cicloLectivo='2020'),  #3
Comision(nroComision=202,cicloLectivo='2020'),  #4
Comision(nroComision=301,cicloLectivo='2020'),  #5
Comision(nroComision=302,cicloLectivo='2020'),  #6
Comision(nroComision=401,cicloLectivo='2020'),  #7
Comision(nroComision=402,cicloLectivo='2020'),  #8
Comision(nroComision=501,cicloLectivo='2020'),  #9
Comision(nroComision=502,cicloLectivo='2020'),  #10
Materia(nombreMateria='Matematica Discreta',anioCursado='1',tipoMateria=''),    #1
Materia(nombreMateria='Algebra',anioCursado='1',tipoMateria=''),    #2
Materia(nombreMateria='Fisica 2',anioCursado='2',tipoMateria=''),   #3
Materia(nombreMateria='Recursos Humanos',anioCursado='3',tipoMateria='Optativa'),   #4
Materia(nombreMateria='Paradigmas',anioCursado='2',tipoMateria=''),     #5
Materia(nombreMateria='Economia',anioCursado='3',tipoMateria=''),       #6
Materia(nombreMateria='Entornos graficos',anioCursado='4',tipoMateria='Optativa'),  #7
Materia(nombreMateria='Legislacion',anioCursado='4',tipoMateria='Optativa'),    #8
Materia(nombreMateria='Probabilidad y Estadistica',anioCursado='3',tipoMateria=''), #9
Materia(nombreMateria='Sistemas de Gestion',anioCursado='5',tipoMateria=''),    #10
Materia(nombreMateria='Inteligencia Artificial',anioCursado='5',tipoMateria=''),    #11
Materia(nombreMateria='Soporte',anioCursado='4',tipoMateria='Optativa'),    #12
ComisionMateria(horarioTeoria = '10:30' ,   #1
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
ComisionMateria(horarioTeoria = '10:30' ,   #2
    diaTeoria = 'Martes',
    aulaTeoria = '102',
    horarioPractica = '10:30',
    diaPractica = 'Viernes',
    aulaPractica = '102',
    profesorT = 'Mario',
    email_profesorT = 'mario@gmail.com',
    profesorP= 'Pedro',
    email_profesorP= 'pedro@gmail.com',
    materia_id =1 ,
    comision_id = 2),
ComisionMateria(horarioTeoria = '7:00' ,    #3
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
    comision_id = 5),
    ComisionMateria(horarioTeoria = '9:30' ,    #4
    diaTeoria = 'Martes',
    aulaTeoria = '108',
    horarioPractica = '11:20',
    diaPractica = 'Lunes',
    aulaPractica = '108',
    profesorT = 'Carla',
    email_profesorT = 'carla@gmail.com',
    profesorP= 'Maria',
    email_profesorP= 'maria@gmail.com',
    materia_id =4 ,
    comision_id = 6),
ComisionMateria(horarioTeoria = '07:15' ,   #5
    diaTeoria = 'Lunes',
    aulaTeoria = '201',
    horarioPractica = '07:15',
    diaPractica = 'Miercoles',
    aulaPractica = '201',
    profesorT = 'Laura',
    email_profesorT = 'laura@gmail.com',
    profesorP= 'Alberto',
    email_profesorP= 'alberto@gmail.com',
    materia_id =3 ,
    comision_id = 3),
ComisionMateria(horarioTeoria = '14:15' ,   #6
    diaTeoria = 'Lunes',
    aulaTeoria = '201',
    horarioPractica = '14:15',
    diaPractica = 'Miercoles',
    aulaPractica = '201',
    profesorT = 'Laura',
    email_profesorT = 'laura@gmail.com',
    profesorP= 'Emilia',
    email_profesorP= 'emilia@gmail.com',
    materia_id =3 ,
    comision_id = 4),
ComisionMateria(horarioTeoria = '13:45' ,   #7
    diaTeoria = 'Jueves',
    aulaTeoria = '501',
    horarioPractica = '-',
    diaPractica = '-',
    aulaPractica = '-',
    profesorT = 'Carlos',
    email_profesorT = 'carlos@gmail.com',
    profesorP= '-',
    email_profesorP= '-',
    materia_id =7 ,
    comision_id = 7),
ComisionMateria(horarioTeoria = '17:45' ,   #8
    diaTeoria = 'Lunes',
    aulaTeoria = '501',
    horarioPractica = '-',
    diaPractica = '-',
    aulaPractica = '-',
    profesorT = 'Carlos',
    email_profesorT = 'carlos@gmail.com',
    profesorP= '-',
    email_profesorP= '-',
    materia_id =7 ,
    comision_id = 8),
ComisionMateria(horarioTeoria = '9:30' ,    #9
    diaTeoria = 'Lunes',
    aulaTeoria = '310',
    horarioPractica = '9:30',
    diaPractica = 'Martes',
    aulaPractica = 'Lab. Lenguajes 2',
    profesorT = 'Alberto',
    email_profesorT = 'alberto@gmail.com',
    profesorP= 'Juan',
    email_profesorP= 'juan@gmail.com',
    materia_id =6 ,
    comision_id = 5),
ComisionMateria(horarioTeoria = '12:45' ,   #10
    diaTeoria = 'Miercoles',
    aulaTeoria = '305',
    horarioPractica = '15:00',
    diaPractica = 'Jueves',
    aulaPractica = 'Lab. Lenguajes 1',
    profesorT = 'Maria',
    email_profesorT = 'maria@gmail.com',
    profesorP= 'Juan',
    email_profesorP= 'juan@gmail.com',
    materia_id =6 ,
    comision_id = 6),
ComisionMateria(horarioTeoria = '11:20' ,   #11
    diaTeoria = 'Miercoles',
    aulaTeoria = '502',
    horarioPractica = '11:20',
    diaPractica = 'Viernes',
    aulaPractica = '502',
    profesorT = 'Luis',
    email_profesorT = 'luis@gmail.com',
    profesorP= '-',
    email_profesorP= '-',
    materia_id =10 ,
    comision_id = 9),
ComisionMateria(horarioTeoria = '18:20' ,   #12
    diaTeoria = 'Miercoles',
    aulaTeoria = '502',
    horarioPractica = '17:00',
    diaPractica = 'Miercoles',
    aulaPractica = '502',
    profesorT = 'Luis',
    email_profesorT = 'luis@gmail.com',
    profesorP= '-',
    email_profesorP= '-',
    materia_id =10 ,
    comision_id = 10),
ComisionMateria(horarioTeoria = '13:10' ,   #13
    diaTeoria = 'Martes',
    aulaTeoria = '401',
    horarioPractica = '14:30',
    diaPractica = 'Miercoles',
    aulaPractica = '401',
    profesorT = 'Mario',
    email_profesorT = 'mario@gmail.com',
    profesorP= 'Juan',
    email_profesorP= 'juan@gmail.com',
    materia_id =12 ,
    comision_id = 1),
ComisionMateria(horarioTeoria = '18:20' ,   #13
    diaTeoria = 'Jueves',
    aulaTeoria = '402',
    horarioPractica = '16:50',
    diaPractica = 'Lunes',
    aulaPractica = '402',
    profesorT = 'Mario',
    email_profesorT = 'mario@gmail.com',
    profesorP= 'Juan',
    email_profesorP= 'juan@gmail.com',
    materia_id =12 ,
    comision_id = 2),
AlumnoComisionMateria(alumno_id=1 ,comision_materia_id=1),
AlumnoComisionMateria(alumno_id=2 ,comision_materia_id=5),
AlumnoComisionMateria(alumno_id=3 ,comision_materia_id=7)
    ])

session.commit()