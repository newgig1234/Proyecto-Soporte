from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship,backref

from base import Base

class Material(Base):
    __tablename__ = 'materiales'
    #Relacionado con materia. material de estudio de la catedra
    idMaterial = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(String)
    linkMaterial = Column(String)
    
    material_id = Column(Integer, ForeignKey('materiales.idMaterial'))
    materia = relationship('Materia', backref=backref('material', uselist=True))

    def __init__(self,descripcion,linkMaterial):
        self.descripcion = descripcion
        self.linkMaterial = linkMaterial
    