from sqlalchemy import Column,String,Integer

from base import Base

class Intitucion(Base):
    __tablename__ = 'instituciones'
    idEdificio = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(String)
    direccion = Column(String)
    telefonoInstitucion = Column(String)
    contacto = Column(String)
    #contacto = persona

    def __init__(self,descripcion,direccion,telefonoInstitucion,contacto): 
        self.descripcion = descripcion
        self.direccion = direccion       
        self.telefonoInstitucion = telefonoInstitucion
        self.contacto = contacto