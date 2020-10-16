from sqlalchemy import Column,Integer,Date,Time, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

class Modulo(Base):
    __tablename__ = 'modulos'
    #dias y horarios en los que se cursa, en determinada aula
    idModulo = Column(Integer, primary_key=True, nullable=False)
    horarioInicio = Column(Time, nullable=False)
    horarioFin = Column(Time, nullable=False)
    dia = Column(Date, nullable=False)
    aula = Column(String, nullable=False)

    clases_comision_id = Column(Integer, ForeignKey('clases.comision_id'))
    clases_materia_id = Column(Integer, ForeignKey('clases.materia_id'))
    clase = relationship('Clses', backref=backref('modulo', uselist=True))

    def __init__(self,horario,dia,aula):
        self.horario=horario
        self.dia=dia
        self.aula=aula