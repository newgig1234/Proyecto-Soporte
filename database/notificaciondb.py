from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship,backref
from sqlalchemy.sql.sqltypes import Date

from base import Base

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    idNotificacion = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    asuntoNot = Column(String)
    contenidoNot = Column(String, nullable=False)
    fechaNot = Column(Date, nullable=False) 

    alumnos = relationship('Persona', secondary='alumno_notificacion')

    docente_id = Column(Integer, ForeignKey('personas.idPersona'))
    docente = relationship('Persona', backref=backref('notificacion', uselist=True))

    materia_id = Column(Integer, ForeignKey('materias.idMateria'))
    materia = relationship('Materia', backref=backref('notificacion', uselist=True))

class AlumnoNotificacion(Base):
    __tablename__ = 'alumno_notificacion'
    notificacion_id = Column(Integer, ForeignKey('notificaciones.idNotificacion'), primary_key=True)
    alumno_id = Column(Integer, ForeignKey('personas.idPersona'), primary_key=True)
