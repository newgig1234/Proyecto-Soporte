from main2 import LoginWindow
from typing import final
from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time
import sqlalchemy
from sqlalchemy.orm import relationship,backref
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

#importar de archivo Datos.py las tablas

Base= declarative_base()
global USER

class Datos(object):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.bind=engine
        db_Session=sessionmaker()
        db_Session.bind=engine
        self.session=db_Session()

    def alta(self,entrada):
        self.session.add(entrada)
        self.session.commit()
        return True

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False))
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    legajo = Column(Integer,nullable=False) #id login
    #username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    clases = relationship('Clases', secondary='alumnos_clases')

    def __repr__(self):
        return f'User {self.name} {self.surname}'
        
            
class AlumnosClases(Base):
    __tablename__ = 'alumnos_clases'
    alumno_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    clases_comision_id = Column(Integer, ForeignKey('clases.comision_id'),primary_key=True)
    clases_materia_id = Column(Integer, ForeignKey('clases.materia_id'),primary_key=True)

class Materia(Base):
    __tablename__ = 'Materias'
    idMateria = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreMateria = Column(String)
    profesor = Column(String)
    email_profesor = Column(String)
    tipoMateria=Column(String) #si es electiva o no

    comisiones = relationship('Comisiones', secondary='clases')

    def __init__(self,nombreMateria,profesor,email_profesor,tipoMateria):
        self.nombreMateria=nombreMateria
        self.profesor=profesor
        self.email_profesor=email_profesor
        self.tipoMateria=tipoMateria

    def __repr__(self):
        return f'Materia {self.nombreMateria}'

    def agregarMateria(self):
        pass


class Comision(Base):
    #cambiar en md
    __tablename__ = 'comisiones'
    idComision = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcion = Column(String)
    cicloLectivo = Column(Integer, nullable=False)
    materias = relationship('Materia', secondary='clases')

    def __init__(self,descripcion,cicloLectivo):
        self.descripcion=descripcion
        self.cicloLectivo=cicloLectivo

class Clase(Base):
    __tablename__ = 'clases'
    comision_id = Column(Integer, ForeignKey('comisiones.idComision'), primary_key=True)
    materia_id = Column(Integer, ForeignKey('materias.idMateria'), primary_key=True)

    alumnos = relationship('Alumnos', secondary='alumnos_clases')

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

    def __init__(self,horaIni,horaFin,dia,aula):
        self.horarioInicio = horaIni
        self.horarioFin = horaFin
        self.dia=dia
        self.aula=aula
#--------------------------------------------------------------------------------------------------------
class Error(Popup):
    error= BoxLayout(orientation='vertical')
    def __init__(self,msj, **kwargs):
        error = BoxLayout(orientation="vertical")
        super(Popup, self).__init__(**kwargs)
        self.add_widget(error)
        self.error = error
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release=self.cerrar)
        self.error.add_widget(mensaje)
        self.error.add_widget(btn)
        
    def cerrar(self,ev):
        self.dismiss()

class Exito(Popup):
    exito= BoxLayout(orientation='vertical')
    def __init__(self,msj, **kwargs):
        exito = BoxLayout(orientation="vertical")
        super(Popup, self).__init__(**kwargs)
        self.add_widget(exito)
        self.error = exito
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release=self.cerrar)
        self.error.add_widget(mensaje)
        self.error.add_widget(btn)
        
    def cerrar(self,ev):
        self.dismiss()

class WindowManager(ScreenManager):
    pass

class LoginWindow(Screen):
    legajo=ObjectProperty()
    password=ObjectProperty()

    def login(self,usu,psw):
        if (usu!='' and psw!=''):
            x = self.datos.validaUsuario(usu,psw) #validar usuario en tabal usuarios
            if not (x==0):
                global us
                us= str(x[0].usuario)
                sm.current= 'mp'
            else:
                er= Error('Usuario y/o contrasena incorrecta', title='Error',size_hint=(None,None),size=(600,200))
                er.open()
        else:
            er= Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()

class RegistroWindow(Screen):
    legajoReg = ObjectProperty(None)
    nombreReg = ObjectProperty(None)
    apellidoReg = ObjectProperty(None)
    emailReg = ObjectProperty(None)
    constrasenaReg = ObjectProperty(None)
    contrasena2Reg = ObjectProperty(None)
    
    def cargarUsuario(self,legajo,nombre,apellido,email,cont1,cont2):
        if(legajo!='' or nombre!='' or apellido!='' or email!='' or cont1!='' or cont2!=''):
            if(cont1 == cont2):
                x= self.Datos.registrarUsuario(legajo,nombre,apellido,email,cont1) #registrar ususario en tabal usuarios
                ex= Exito('Se registro el usuario con exito',title='Exito',size_hint=(None,None),size=(600,200))
                ex.open()
                sm.current='login'
            else:
                er= Error('Las contraseñas son diferentes', title='Error',size_hint=(None,None),size=(600,200))
                er.open()
        else:
            er= Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()
            
class MenuPrincipal(Screen):

    def materiasBtn(self):
        sm.current='mat'

    def editarMateriasBtn(self):
        sm.current='em'

    def editarPerfilBtn(self):
        sm.current='edp'

    def logOut(self):
        #confirmacionSalir()
        pass

class AgregarMateria(Screen):
    cont=0
    m1=ObjectProperty(None)
    c1=ObjectProperty(None)

    
class Materias(Screen):#

    pass

class InfoMateria(Screen):
    pass

    def volverBtnIm(self):
        sm.current='mat'

class EditarPerfil(Screen):#traer de la base de datos los datos del perfil, ponerlos en un text imput y si los queire cambiar que los cambie
    pass

    def volverBtnEp(self):
        sm.current='mp'

    def confirmarBtnEp(self):
        sm.current='mp'

#----------------------------------------------------------------------------------------------------
kivy.require("1.11.0")
kv = Builder.load_file('interfaces.kv')
sm = WindowManager()

screens = [LoginWindow(name="login"), RegistroWindow(name="registro"), MenuPrincipal(name="mp"),
            AgregarMateria(name='am'),Materias(name='mat'),InfoMateria(name='im'),EditarPerfil(name='ep'),]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class TpMainApp(App):
    def build(self):
        self.title = 'TPI'
        return sm

if __name__ == "__main__":
    TpMainApp().run()