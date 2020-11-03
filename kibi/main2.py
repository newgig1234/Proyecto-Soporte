#from bleach.linkifier import EMAIL_RE
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#from kivy.uix.textinput import TextInput
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from prompt_toolkit.shortcuts.dialogs import button_dialog
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
#from kivymd.theming import ThemeManager
#from database import DataBase
#db = DataBase("users.txt")

# ------------------------------------------------------------------------------------
# CLASES

class WindowManager(ScreenManager):
    pass

class LoginWindow(Screen):
    legajo = ObjectProperty(None)
    contrasena = ObjectProperty(None)

    '''def login(self):
        if db.validate(self.legajo.text, self.contrasena.text):
            MainWindow.current = self.legajo.text
            self.reset()
            sm.current = "mp"
        else:
            invalidLogin()'''
    
    def login(self):
        if self.validarUsuarioDB():
            self.reset()
            sm.current='mp'
        else:
            invalidLogin()

    def registroBtn(self):
        self.reset()
        sm.current = "registro"

    def reset(self):
        self.legajo.text = ""
        self.contrasena.text = ""

    def validarUsuarioDB(self):#concetar a la base de datos y hacer comprobacion
        try:
            pass
        except:
            pass
        finally:
            pass

# clase para registrarse en la app


class RegistroWindow(Screen):
    legajoReg = ObjectProperty(None)
    nombreReg = ObjectProperty(None)
    apellidoReg = ObjectProperty(None)
    emailReg = ObjectProperty(None)
    constrasenaReg = ObjectProperty(None)
    contrasena2Reg = ObjectProperty(None)

    def aceptar(self):
        if self.controlLegajo(self.legajoReg.text) and self.controlNA(self.nombreReg.text) and self.controlNA(self.apellidoReg.text) and self.controlNA(self.contrasenaReg.text) and self.controlNA(self.contrasena2Reg.text) and self.controlMail(self.emailReg.text):
            if self.contrasenaReg.text == self.contrasena2Reg.text:
                self.controlDB()
                self.reset()
                sm.current = 'login'
            else:
                invalidContrasena()
        else:
            invalidFormulario()

    def login(self):
        self.reset()
        sm.current = 'login'

    def reset(self):
        self.legajoReg.text = ''
        self.nombreReg.text = ''
        self.apellidoReg.text = ''
        self.emailReg.text = ''
        self.constrasenaReg.text = ''
        self.contrasena2Reg.text = ''

    
    def controlLegajo(self, legR):#ademas, verificar si el legajo es valido
        if legR != '' and 1 < int(legR) < 100000:
            return True
        else:
            pass

    def controlNA(self, na):#verifica qeu sea un nombre valido
        if len(na) > 2 and na != '':
            return True

    def controlMail(self, mailC):#verifica qeu sea un mail valido
        if mailC.text.count('@') == 1 and mailC.text.count('.') > 1 and mailC != '' and len(mailC) > 6:
            return True

    def controlDB(self):
        return True

# modificar


class MenuPrincipal(Screen):
    #crea botones que hacen la transferencia de pantalla
    def mapaBtn(self):
        sm.current='mp'

    def materiasBtn(self):
        sm.current='mat'

    def editarMateriasBtn(self):
        sm.current='em'

    def consultasBtn(self):
        sm.current='con'

    def bibliografiaBtn(self):
        sm.current='bl'

    def editarPerfilBtn(self):
        sm.current='edp'

    def noticiasBtn(self):
        sm.current='not'

    def logOut(self):
        confirmacionSalir()

class AgregarMateria(Screen):#se agrega una materia a las que cursa el alumno
    #se tienen que traer todas las materias pertenecientes a una carrera en la BD y que el alumno no este anotado o este aprobado/regular/cursando
    #para que se seleccione con una lista desplegable y se inscriba, posteriormente se debera seleccionar la comision.
    cont=0
    m1=ObjectProperty(None)
    c1=ObjectProperty(None)


    pass
    def omitirBtn(self):#se vuelve atras sin agregar materias, hacer un reset
        pass

    def aceptarBtn(self):#se agrega la materia
        sm.current='mp'
        pass

    '''def agregarBtn(self):
        materia= TextInput(text='materia',id=crearidmat(cont))
        comision= TextInput(text='comision',id=crearidcom(cont))
        sacar= Button(text='X',id=crearidbtn(cont))
        self.cont = cont +1
        self.root.ids.grid_am.add_widget(materia)
        self.root.ids.grid_am.add_widget(comision)
        self.root.ids.grid_am.add_widget(sacar)'''


class Materias(Screen):
    pass

class Consulta(Screen):
    '''se escribe una consulta a una materia (con su comision y su profesor correspondiente), un vez contestada quedara guardada
    para que todos los alumnos de esa comision la puedan ver (ver si se puede hacer con ejercicios resueltos y que queden guadrados
    para futuras comisiones. Resumiendo: guardar los ejercicios resueltos y la consulta)
    '''
    consultaC= ObjectProperty(None)
    pass

    def btnVolverCon(self):
        sm.current='mp'
        self.reset()
        pass

    def reset(self):
        self.consultaC.text=''
        pass

class InfoMateria(Screen):
    '''Mostrar donde se cursa una materia (aula) y los horarios -> depende de la comision y el ciclo lectivo
    
    '''
    pass

    def volverBtnIm(self):
        sm.current='mat'

class EditarPerfil(Screen):
    '''traer de la base de datos los datos del perfil, ponerlos en un text imput y si se desean cambiar los datos, debera modificarlos 
    en el input'''
    
    pass

    def volverBtnEp(self):
        sm.current='mp'

    def confirmarBtnEp(self):
        sm.current='mp'
        #modificar BD

class Mapa(Screen):
    '''imagenes que muestran donde esta ubicada cada aula del establecimiento (piso y nro de aula)'''
    pass

class Bibliografia(Screen):
    '''Bibliografia perteneciente a una materia, los jefes de area deberian poder cargarla en la base de datos para el posterior uso de los alumnos'''
    pass

class Noticias(Screen):
    ''''''
    pass

class InfoNoticia(Screen):
    ''''''
    pass

    def volverBtnIn(self):
        sm.current='not'

'''Ver uso de RecycleView y evaluar si se puede utilizar dentro del tipo de dato Screen'''
class RVmaterias(RecycleView):
    def __init__(self,**kwargs):
        super(RVmaterias,self).__init__(**kwargs)
        self.data= buscarMaterias()

class NotRV(RecycleView):
    def __init__(self,**kwargs):
        super(NotRV,self).__init__(**kwargs)
        self.data= buscarNoticias()

class misNoticias(BoxLayout):
    
    def irBtn():
        pass

# ------------------------------------------------------------------------------
# FUNCIONES SUELTAS

def buscarMaterias():
    return 1

def buscarNoticias():
    return 1

# popup que muestra que las contrasenas son invalidas para en el registro
def invalidContrasena():
    pop = Popup(title='Contrasena inválida.',
                content=Label(text='Las contrasenas no coinciden.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

# popup que muestra que faltan llenar datos o que los datos son incorrectos en el formulario
def invalidFormulario():
    pop = Popup(title='Formulario inválido',
                content=Label(
                    text='Por favor complete las casillas con los valores correctos.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

#Confirmacion para salir del menu principal
def confirmacionSalir():
    box= BoxLayout(orientation='vertical',padding=(10))
    box.add_widget(Label(text='Salir al menú principal?'))
    btn1=Button(text='Salir')
    btn2=Button(text='Continuar aquí')
    box.add_widget(btn1)
    box.add_widget(btn2)
    
    pop=Popup(title='Salir a página de inicio?',content=box,auto_dismiss=False)

    btn1.bind(on_release=sm.current('login'))
    btn2.bind(on_release=sm.current('mp'))

    pop.open()
#-----------------------------------------------------
#CONEXION A BD Y CONTROLES ADICIONALES
def invalidLogin():
    pass

def conectDB():
    pass

#--------------------------------------------------
#PROGRAMA PRINCIPAL Y DATOS NECESARIOS PARA INICIALIZACION DEL PROGRAMA
kivy.require("1.11.0")
kv = Builder.load_file('interfaces.kv')
sm = WindowManager()

# Se agregan todas las ventanas que van en el programa
screens = [LoginWindow(name="login"), RegistroWindow(name="registro"), MenuPrincipal(name="mp"),AgregarMateria(name='am'),Materias(name='mat'),Consulta(name='con'), InfoMateria(name='im'),
        EditarPerfil(name='ep'), Mapa(name='mp'),Bibliografia(name='bl'),Noticias(name='not'),InfoNoticia(name='in')]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class TpMainApp(App):
    def build(self):
        self.title = 'TPI'
        return sm


if __name__ == "__main__":
    TpMainApp().run()