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
from sqlalchemy.sql.elements import Null

from Datos import Alumno,Materia,Comision,AlumnoComisionMateria,ComisionMateria

class Error(Popup):
    error= BoxLayout(orientation='vertical')
    def __init__(self,msj, **kwargs):
        error = BoxLayout(orientation="vertical")
        #super(Popup, self).__init__(**kwargs)
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
        #super(Popup, self).__init__(**kwargs)
        self.add_widget(exito)
        self.exito = exito
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release=self.cerrar)
        self.exito.add_widget(mensaje)
        self.exito.add_widget(btn)
        
    def cerrar(self,ev):
        self.dismiss()

class MostrarMaterias(Popup):
    mostrar_materia= BoxLayout(orientation='vertical')
    def __init__(self, **kwargs):
        pass

    def construir(self):
        mensaje = Label(text = 'MIS MATERIAS')
        self.add_widget(mensaje)
        mostrar_materia_Gridlayout = GridLayout(col=1)
        self.add_widget(mostrar_materia_Gridlayout)
        mats = self.AlumnoComisionMateria.traerMateriasAlumno(us)
        for matcom in mats:
            btn = Button(text = matcom.materia.nombreMateria)
            mi = MostrarInformacion()
            btn.bind(on_release=mi.construir(matcom))
            self.mostrar_materia_Gridlayout.add_widget(btn)
        volver = Button(text='Atras')
        volver.bind(on_release=self.cerrar)
        self.mostrar_materia_Gridlayout.add_widget(volver)
        
    def cerrar(self,ev):
        self.dismiss()

class MostrarInformacion(Popup):
    def __init__(self, **kwargs):
        pass
        
    def cosntruir(self,matcom):
        box= BoxLayout(orientation='verticla')
        mensaje= Label(text='INFORMACION MATERIA')#modificar altura
        box.add_widget(mensaje)
        mostrar_informacion_Gridlayout = GridLayout(Col=8)# no lo toma
        box.add_widget(mostrar_informacion_Gridlayout)
        nm,nc = self.ComisionMateria.infoMat(matcom)
        nombreMateria = Label(text=nm)
        numComision = Label(text=nc) 
        horaT = Label(text=matcom.horarioTeoria)
        diaT = Label(text=matcom.diaTeoria)
        aulaT= Label(text=matcom.aulaTeoria)
        horaP= Label(text=matcom.horaPractica)
        diaP= Label(text=matcom.diaPractica)
        aulaP=  Label(text=matcom.aulaPractica)
        self.mostrar_informacion_Gridlayout.add_widget(nombreMateria)
        self.mostrar_informacion_Gridlayout.add_widget(numComision)
        self.mostrar_informacion_Gridlayout.add_widget(horaT)
        self.mostrar_informacion_Gridlayout.add_widget(diaT)
        self.mostrar_informacion_Gridlayout.add_widget(aulaT)
        self.mostrar_informacion_Gridlayout.add_widget(horaP)
        self.mostrar_informacion_Gridlayout.add_widget(diaP)
        self.mostrar_informacion_Gridlayout.add_widget(aulaP)


class WindowManager(ScreenManager):
    pass

class LoginWindow(Screen):
    legajo = ObjectProperty()
    password = ObjectProperty()

    def login(self,usu,psw):
        if (usu!='' and psw!=''):
            x = self.Alumno.validaUsuario(usu,psw) #validar usuario en tabal usuarios
            if (x):
                global us
                us = x
                #us= str(x[0].usuario)
                sm.current= 'mp'
            else:
                er= Error('Usuario y/o contrasena incorrecta', title='Error',size_hint=(None,None),size=(600,200))
                er.open()
                sm.current= 'login'
        else:
            er= Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()
            sm.current= 'login'
    
    def registroBtn(self):
        sm.current = 'registro'

class RegistroWindow(Screen):
    legajoReg = ObjectProperty(None)
    nombreReg = ObjectProperty(None)
    apellidoReg = ObjectProperty(None)
    emailReg = ObjectProperty(None)
    constrasenaReg = ObjectProperty(None)
    contrasena2Reg = ObjectProperty(None)
    
    def cargarUsuario(self,leg,nom,app,mail,cont1,cont2):
        if(leg!='' or nom!='' or app!='' or mail!='' or cont1!='' or cont2!=''):
            if(cont1 == cont2):
                self.Alumno.altaUsuario(Alumno(legajo=leg,nombre=nom,apellido=app,email=mail,password=cont1)) #registrar ususario en tabal usuarios
                ex= Exito('Se registro el usuario con exito',title='Exito',size_hint=(None,None),size=(600,200))
                ex.open()
                sm.current='login'
            else:
                er= Error('Las contraseñas son diferentes', title='Error',size_hint=(None,None),size=(600,200))
                er.open()
        else:
            er= Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()
    def volver_login(self):
        sm.current = 'login'

class MenuPrincipal(Screen):

    def materiasBtn(self):
        mm = MostrarMaterias()
        mm.construir()

    def editarMateriasBtn(self):
        sm.current='em'

    def editarPerfilBtn(self):
        sm.current='edp'

    def logOut(self):
        #confirmacionSalir()
        pass

class AgregarMateria(Screen):
    #cont=0
    #m1=ObjectProperty(None)
    #c1=ObjectProperty(None)
    pass

    
class Materias(Screen):#generar dinamicamente la lista de  materias a las que se puede inscribir el alumno
    pass

# class InfoMateria(Screen):#mostrar informacion de una materia
#     def volverBtnIm(self):
#         sm.current='mat'

class EditarPerfil(Screen):#traer de la base de datos los datos del perfil, ponerlos en un text imput y si los queire cambiar que los cambie
    pass

    def volverBtnEp(self):
        sm.current='mp'

    def confirmarBtnEp(self):
        sm.current='mp'

class SeleccionarMateria(Popup):
    seleccionMateria=BoxLayout(orientation='vertical')
    def __init__(self, **kwargs):
        #seleccionMateria=BoxLayout(orientation='vertical')
        #super(Popup, self).__init__(**kwargs)
        self.add_widget(self.root)

    def buscarMaterias(self):
        #materias_a_inscribir = Materia.buscar_materias()
        #return materias_a_inscribir
        pass

class SeleccionarComision(Popup):
    def __init__(self, **kwargs):
        #super(Popup, self).__init__(**kwargs)
        self.add_widget(self.root)

    def buscarComisionMateria(self):#buscar una comision perteneciente a una materia
        pass

class InfoMateria(Popup):
    def __init__(self, **kwargs):
        #super(Popup, self).__init__(**kwargs)
        self.add_widget(self.root)

    def mostrarInformacionMateria(self):#muestra la informacion de una materia
        pass
    
#----------------------------------------------------------------------------------------------------
kivy.require("1.11.0")
kv = Builder.load_file('interfaces.kv')
sm = WindowManager()

screens = [LoginWindow(name="login"), RegistroWindow(name="registro"), MenuPrincipal(name="mp"),
            AgregarMateria(name='am'),Materias(name='mat'),InfoMateria(name='im'),EditarPerfil(name='ep'),]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

us=Null
class TpMainApp(App):
    def build(self):
        self.title = 'TPI'
        return sm

if __name__ == "__main__":
    TpMainApp().run()