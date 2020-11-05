import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sqlalchemy.sql.elements import Null

from Datos import Alumno,Materia,Comision,AlumnoComisionMateria,ComisionMateria
kivy.require("1.11.0")
#-------------------------------------------------------------------------------------- https://meet.google.com/iqs-ksip-jta
class Error(Popup):
    #error= BoxLayout(orientation='vertical')
    def __init__(self,msj, **kwargs):
        super().__init__(**kwargs)
        self.error = BoxLayout(orientation="vertical")
        self.add_widget(self.error)
        #self.error = error
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release= lambda x:  self.cerrar)
        self.error.add_widget(mensaje)
        self.error.add_widget(btn)
        
    def cerrar(self,ev):
        self.error.dismiss()

class Exito(Popup):
    #exito= BoxLayout(orientation='vertical')
    def __init__(self,msj, **kwargs):
        super().__init__(**kwargs)
        self.exito = BoxLayout(orientation="vertical")
        self.add_widget(self.exito)
        #self.exito = exito
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release= lambda x:  self.cerrar)
        self.exito.add_widget(mensaje)
        self.exito.add_widget(btn)
        
    def cerrar(self,ev):
        self.exito.dismiss()

class MostrarMaterias:

    def build(self,u):
        #self.construir(u).open()

        #def construir(self,u):
        box= BoxLayout(orientation='vertical',padding=10)
        box.clear_widgets()
        gLayout= GridLayout(cols=1,padding=10)
        gLayout.clear_widgets()
        acm= AlumnoComisionMateria()
        mats= acm.traerMateriasAlumno(u)
        #mats = AlumnoComisionMateria.traerMateriasAlumno(u)
        mi = MostrarInformacion()
        if not(mats):
            for matcom in mats:
                btn = Button(text = matcom.materia.nombreMateria)
                btn.bind(on_release= lambda x:  mi.build(matcom,u))
                gLayout.add_widget(btn)
        btnVolver = Button(text='Atras')
        btnVolver.bind(on_release= self.cerrar)
        box.add_widget(gLayout)
        box.addwidget(btnVolver)
        self.pop=Popup(Title='Mis Materias',content=box,padding=5)
        self.pop.open()
        
    def cerrar(self):
        self.pop.dismiss()

class MostrarInformacion:

    def build(self,matcom,u):
        #self.construir(mc,u).open()    
    #def construir(self,matcom,u):
        box= BoxLayout(orientation='vertical')
        box.clear_widgets()
        gLayout=GridLayout(cols=2,padding=5)
        gLayout.clear_widgets()
        comMat= ComisionMateria()
        nomMateria,numeroComision = comMat.infoMat(matcom)
        btnBaja= Button(text='Darse de baja de una materia')
        btnBaja.bind(on_release= lambda x:  self.darBajaMaeteria(matcom,u))
        mm = MostrarMaterias()
        btnAtras=Button(text='Volver')
        btnAtras.bind(on_release= lambda x:  mm.build(u))
        nom=Label(text='Nombre')
        num=Label(text='Numero Comision')
        ht=Label(text='Hora Teoria')
        dt=Label(text='Dia Teoria')
        at=Label(text='Aula Teoria')
        hp=Label(text='Hora Practica')
        dp=Label(text='Dia Practica')
        ap=Label(text='Aula Practica')
        nombreMateria = Label(text=nomMateria)
        numComision = Label(text=numeroComision) 
        horaT = Label(text=matcom.horarioTeoria)
        diaT = Label(text=matcom.diaTeoria)
        aulaT = Label(text=matcom.aulaTeoria)
        horaP = Label(text=matcom.horaPractica)
        diaP = Label(text=matcom.diaPractica)
        aulaP =  Label(text=matcom.aulaPractica)
        gLayout.add_widget(nom)
        gLayout.add_widget(nombreMateria)
        gLayout.add_widget(num)
        gLayout.add_widget(numComision)
        gLayout.add_widget(ht)
        gLayout.add_widget(horaT)
        gLayout.add_widget(dt)
        gLayout.add_widget(diaT)
        gLayout.add_widget(at)
        gLayout.add_widget(aulaT)
        gLayout.add_widget(hp)
        gLayout.add_widget(horaP)
        gLayout.add_widget(dp)
        gLayout.add_widget(diaP)
        gLayout.add_widget(ap)
        gLayout.add_widget(aulaP)
        box.add_widget(gLayout)
        box.add_widget(btnAtras)
        box.add_widget(btnBaja)
        self.pop = Popup(Title='Mostrar Informacion',content=box,padding=10)
        self.pop.open()

    def darBajaMaeteria(self,mc,u):
        amc = AlumnoComisionMateria().bajaMateria(u,mc)#ver esto
        if amc == True:
            ex= Exito('Se elimino la materia de su lista correctamente.',title='Exito',size_hint=(None,None),size=(600,200))
            ex.open()
            ex.dismiss()
            mm = MostrarMaterias()
            mm.build(u)
        else:
            er= Error('No se pudo eliminar la materia de su lista, por favor intente nuevamente.', title='Error',size_hint=(None,None),size=(600,200))
            er.open()
            er.dismiss()

class loginPopup:
    
    def build(self):
        #self.construir().open()

    #def construir(self):
        box= BoxLayout(orientation='vertical', padding=5)
        txt= Label(text='Login')
        gLayout=GridLayout(cols=2, padding=10)
        txtUser=Label(text='Legajo')
        txtPsw=Label(text='Contrasena')
        txtIUser= TextInput(multiline=False)
        txtIPsw= TextInput(multiline=False, password=True)
        btn= Button(text='Ingresar')
        btn.bind(on_release= lambda x:  self.controlLogin(txtIUser.text,txtIPsw.text))#funcion para logear
        btnR=Button(text='Registrarse')
        btnR.bind(on_release= lambda x:  self.irRegistro())#boton REgistro
        gLayout.add_widget(txtUser)
        gLayout.add_widget(txtIUser)
        gLayout.add_widget(txtPsw)
        gLayout.add_widget(txtIPsw)
        box.add_widget(txt)
        box.add_widget(gLayout)
        box.add_widget(btn)
        box.add_widget(btnR)
        self.pop = Popup(title='Login',content=box, padding=5)
        self.pop.open()

    def irRegistro(self):
        reg = registroPop()
        reg.build()
    
    def controlLogin(self,leg:str,psw:str):
        if (leg!='' and psw!=''):
            a= Alumno()
            x = a.validarUsuario(leg,psw) #validar usuario en tabal usuarios
            if (x != None):#ver que onda esto
                mp = MenuPrincipal()
                mp.build(x)
            else:
                er = Error('Usuario y/o contrasena incorrecta', title='Error',size_hint=(None,None),size=(600,200))
                er.open()

        else:
            er = Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()

class MenuPrincipal:

    def build(self,u):
        #self.construir(us).open()

    #def construir(self,u):
        box = BoxLayout(orientation='vertical',padding=5)
        txt = Label(text='Menu Principal')
        gLayout = GridLayout(cols=1, padding=5)
        btnMaterias = Button(text='Materias')
        btnAgregarMaterias=Button(text='Agregar Materias')
        btnSalir = Button(text='Salir')
        btnMaterias.bind(on_release= lambda x:  self.mostrarMaterias(u))
        btnAgregarMaterias.bind(on_release= lambda x:  self.agregarMateria(u))
        btnSalir.bind(on_release= lambda x:  self.cerrar())
        gLayout.add_widget(btnMaterias)
        gLayout.add_widget(btnAgregarMaterias)
        gLayout.add_widget(btnSalir)
        box.add_widget(txt)
        box.add_widget(gLayout)
        self.pop = Popup(title ='Menu Principal',content=box,padding=5)
        self.pop.open()

    def mostrarMaterias(self,u):
        mm= MostrarMaterias()
        mm.build(u)

    def agregarMateria(self,u):
        ss= SeleccionarMateria()
        ss.build(u)

    def cerrar(self):
        log = loginPopup()
        log.build()

class registroPop:
    def build(self):
        #self.construir().open()

    #def construir(self):
        box= BoxLayout(orientation='vertical',padding=5)
        gLayout= GridLayout(cols=2,padding=5)
        txt= Label(text='Registro')
        btnAceptar=Button(text='aceptar')
        txtLegajo= Label(text='Legajo')
        txtNombre= Label(text='Nombre')
        txtApellido= Label(text='Apellido')
        txtMail=Label(text='Mail')
        txtPsw1= Label(text='Contrasena')
        txtPsw2= Label(text='Repetir Contrasena')
        txtILegajo =TextInput(multiline=False)
        txtINombre= TextInput(multiline=False)
        txtIApellido= TextInput(multiline=False)
        txtIMail=TextInput(multiline=False)
        txtIPsw1= TextInput(password=True, multiline=False)
        txtIPsw2= TextInput(password=True, multiline=False)
        gLayout.add_widget(txtLegajo)
        gLayout.add_widget(txtILegajo)
        gLayout.add_widget(txtNombre)
        gLayout.add_widget(txtINombre)
        gLayout.add_widget(txtApellido)
        gLayout.add_widget(txtIApellido)
        gLayout.add_widget(txtMail)
        gLayout.add_widget(txtIMail)
        gLayout.add_widget(txtPsw1)
        gLayout.add_widget(txtIPsw1)
        gLayout.add_widget(txtPsw2)
        gLayout.add_widget(txtIPsw2)
        btnAceptar.bind(on_release= lambda x:  self.validarUsuario(txtILegajo.text,txtINombre.text,txtIApellido.text,txtIMail.text,txtIPsw1.text,txtIPsw2.text))
        box.add_widget(txt)
        box.add_widget(gLayout)
        box.add_widget(btnAceptar)
        self.pop= Popup(title='Registro', content=box,padding=5)
        self.pop.open()

    def validarUsuario(self,leg,nom,app,mail,cont1,cont2):
        if (4<len(leg)<6 and 5<len(cont1) and 5<len(cont2)):
            if (leg !='' and nom!='' and app!='' and mail!='' and cont1!='' and cont2!=''):
                if(cont1 == cont2):
                    a=Alumno()
                    a.altaUsuario(leg,nom,app,mail,cont1) #instanciar     #registrar ususario en tabal usuarios
                    ex= Exito('Se registro el usuario con exito',title='Exito',size_hint=(None,None),size=(600,200))
                    ex.open()
                    usu = a.buscarUsuario(leg)
                    mp = MenuPrincipal()
                    mp.build(usu)
                else:
                    er= Error('Las contrasenas son diferentes', title='Error',size_hint=(None,None),size=(600,200))
                    er.open()
                    reg = registroPop()
                    reg.build()
            else:
                er1= Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
                er1.open()
        else: 
            er2=Error('Legajo y/o Password no tiene la longitud necesaria', title='Error',size_hint=(None,None),size=(600,200))
            er2.open()
   
class SeleccionarMateria:

    def build(self,u):
        #self.construir(u).open()

    #def construir(self,u):
        box=BoxLayout(orientation='vertical', padding=10)
        txt = Label(text ='MATERIAS')
        gLayout= GridLayout(cols=1, padding=10)
        m=Materia()
        mats = m.traerMaterias()#instanciar
        for mat in mats:
            btn = Button(text = mat.nombreMateria)
            btn.bind(on_release= lambda x:  self.confirmar(mat,u))
            gLayout.add_widget(btn)
        btnAtras=Button(text='Atras')
        btnAtras.bind(on_release= lambda x:  self.cerrar())
        box.add_widget(txt)
        box.add_widget(gLayout)
        box.add_widget(btnAtras)
        self.pop = Popup(title='SelecionarMateria',content=box,padding=10)
        self.pop.open()

    def confirmar(self,m,u):
        box = BoxLayout(orientation='vertical',padding=10)
        gLayout= GridLayout(cols=2,row=1,padding=10)
        txt= Label(text='¿Esta seguro que desea inscribirse a esta materia?')
        btnAceptar = Button(text='Aceptar')
        btnCancelar= Button(text='Cancelar')
        btnAceptar.bind(on_release = lambda x:  self.selecCom(m,u))
        btnCancelar.bind(on_release = lambda x:  self.build(u))
        box.add_widget(txt)
        gLayout.add_widget(btnCancelar)
        gLayout.add_widget(btnAceptar)
        box.add_widget=gLayout
        self.pop = Popup(Title='Confirmar',content=box)
        self.pop.open()

    def selecCom(self,m,u):
        sm = SeleccionarComision()
        sm.build(m,u)
        
    def cerrar(self):
        self.pop.dismiss()

class SeleccionarComision:

    def build(self,mat,u):
        #self.construir(m,u).open()

    #def construir(self,mat,u):
        box= BoxLayout(orientation='horizontal',padding=10)
        txt=Label(text='Seleccione Comision')
        gLayout = GridLayout(cols=2,padding=10)
        c= ComisionMateria()
        comis = c.traerComisiones(mat) #instanciar
        for com in comis:
            btn=Button(text=com.nroComision)
            btn.bind(on_release= lambda x:  self.confirmar(mat,com,u))
            gLayout.add_widget(btn)
        box.add_widget(txt)
        box.add_widget(gLayout)
        self.pop = Popup(title='Seleccionar Materia',content=box)
        self.pop.open()


    def confirmar(self,m,c,u):
        box= BoxLayout(orientation='vertical',padding=10)
        txt= Label(text='¿Desea esta comision, Materia{materia}, Comision{comision}?'.format(materia=m.nombre,comision=c.detalle))
        gLayout= GridLayout(cols=2,padding=10)
        btnCancelar=Button(text='Cancelar')
        btnCancelar.bind(on_release= lambda x:  self.build(m,u))#funcion boton cancelar
        btnAceptar=Button(text='Aceptar')
        btnAceptar.bind(on_release= lambda x:  self.altaACM(m,c,u))#funcion boton aceptar
        box.add_widget(txt)
        gLayout.add_widget(btnCancelar)
        gLayout.add_widget(btnAceptar)
        box.add_widget(gLayout)
        self.pop=Popup(title='Confirmar',content=box)
        self.pop.open()
        #return pop
    
    
    def altaACM(self,m,c,u):
        icm = ComisionMateria()
        cm = icm.devolver(m,c)
        iacm = AlumnoComisionMateria()
        res = iacm.alta(AlumnoComisionMateria(alumno_id=u.id,comision_materia_id=cm.comision_materia_id,alumno=u,comisionmateria=cm))
        if res==True:
            ex= Exito('¡Se agrego la materia con exito!',title='Exito',size_hint=(None,None),size=(600,200))
            ex.open()
            mp = MenuPrincipal()
            mp.build(u)
        else:
            er= Error('No se pudo agregar la materia, intente nuevamente desde el comienzo.', title='Error',size_hint=(None,None),size=(600,200))
            er.open()
            mp = MenuPrincipal()
            mp.build(u)
            
#----------------------------------------------------------------------------------------------------

us=Null
class myAppApp(App):
    def build(self):
        self.title = 'TPI'
        lp = loginPopup()
        return lp.build()

if __name__ == "__main__":
    myAppApp().run()