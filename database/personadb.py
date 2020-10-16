from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship,backref
from sqlalchemy.orm.util import polymorphic_union, with_polymorphic
from sqlalchemy.sql.sqltypes import Boolean
  

from base import Base

class Persona(Base):
    __tablename__ = 'personas'
    idPersona=Column(Integer,primary_key=True, autoincrement=True,nullable=False)
    legajo= Column(Integer, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False)
    contrasena= Column(String, nullable=False)
    esDocente= Column(Boolean, nullable = True)
    
    
    if esDocente == True:
        clases_comision_id = Column(Integer, ForeignKey('clases.comision_id'))
        clases_materia_id = Column(Integer, ForeignKey('clases.materia_id'))
        clase = relationship('Clase', backref=backref('personas', uselist=True))        
    elif esDocente == False:
        clases = relationship('Clases', secondary='alumnosclases')
    
    notificaciones = relationship('Notificacion', secondary='alumno_notificacion')

    # __mapper_args__={
    #     'polymorphic_identity':'persona',
    #     'polymorphic_on': type
    #     }

    def __init__(self,legajo,nombre,apellido,email,contrasena):
        self.legajo=legajo
        self.nombre=nombre
        self.apellido=apellido
        self.email=email
        self.contrasena=contrasena
        self.esDocente=False

class AlumnosClases(Base):
    __tablename__ = 'alumnos_clases'
    persona_id = Column(Integer, ForeignKey('personas.idPersona'), primary_key=True)
    clases_comision_id = Column(Integer, ForeignKey('clases.comision_id'),primary_key=True)
    clases_materia_id = Column(Integer, ForeignKey('clases.materia_id'),primary_key=True)