from copy import deepcopy

import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sqlalchemy.sql.elements import Null
from kivy.properties import NumericProperty


from Datos import Alumno,Materia,Comision,AlumnoComisionMateria,ComisionMateria
kivy.require("1.11.0")

#------------------------------------------------------------------------------------- 
#class myButton()

class Error(Popup):
    def __init__(self,msj, **kwargs):
        super().__init__(**kwargs)
        self.error = BoxLayout(orientation="vertical")
        self.add_widget(self.error)
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release= lambda x:  self.cerrar())
        self.error.add_widget(mensaje)
        self.error.add_widget(btn)
        
    def cerrar(self):
        self.error.dismiss()

class Exito(Popup):

    def __init__(self,msj, **kwargs):
        super().__init__(**kwargs)
        self.exito = BoxLayout(orientation="vertical")
        self.add_widget(self.exito)
        self.construir(msj)

    def construir(self, msj):
        mensaje = Label(text = msj)
        btn = Button(text = "Aceptar")
        btn.bind(on_release= lambda x:  self.cerrar())#se puede modificar para simplificar
        self.exito.add_widget(mensaje)
        self.exito.add_widget(btn)
        
    def cerrar(self):
        self.exito.dismiss()

class MostrarMaterias(Popup):
    def __init__(self,**kwargs):
        super(MostrarMaterias,self).__init__(**kwargs)

    def build(self,u):
        box= BoxLayout(orientation='vertical')
        gLayout= GridLayout(cols=2)
        acm= AlumnoComisionMateria()
        mats= acm.traerMateriasAlumno(u)
        if mats:
            for matcom in mats:
                mi = MostrarInformacion()
                nm = matcom.nombreMat()
                btn = Button(text = nm.nombreMateria)
                btn.bind(on_release= lambda x: mi.build(matcom,u))
                gLayout.add_widget(btn)
        btnVolver = Button(text='Atras')
        btnVolver.bind(on_release= lambda x: self.cerrar())
        box.add_widget(gLayout)
        box.add_widget(btnVolver)
        self.pop= Popup(title='Mis Materias',content=box)
        self.pop.open()
        
    def cerrar(self):
        self.pop.dismiss()

class MostrarInformacion(Popup):
    def __init__(self,**kwargs):
        super(MostrarInformacion,self).__init__(**kwargs)

    def build(self,matcom,u):
        box= BoxLayout(orientation='vertical')
        box.clear_widgets()
        gLayout =GridLayout(cols=2)
        gLayout.clear_widgets()
        comMat = ComisionMateria()
        nomMateria ,numeroComision = comMat.infoMat(matcom)
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
        horaP = Label(text=matcom.horarioPractica)
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
        self.pop = Popup(title='Mostrar Informacion',content=box)
        self.pop.open()

    def darBajaMaeteria(self,mc,u):
        amc = AlumnoComisionMateria().bajaMateria(u,mc)
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

class loginPopup(Popup):
    def __init__(self,**kwargs):
        super(loginPopup,self).__init__(**kwargs)
    
    def build(self):
        box= BoxLayout(orientation='vertical')
        txt= Label(text='Login')
        gLayout=GridLayout(cols=2)
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
        self.pop = Popup(title='Login',content=box)
        self.pop.open()

    def irRegistro(self):
        reg = registroPop()
        reg.build()
    
    def controlLogin(self,leg:str,psw:str):
        if (leg!='' and psw!=''):
            a= Alumno()
            x = a.validarUsuario(leg,psw) #validar usuario en tabal usuarios
            if (x != None):
                mp = MenuPrincipal()
                mp.build(x)
            else:
                er = Error('Usuario y/o contrasena incorrecta', title='Error',size_hint=(None,None),size=(600,200))
                er.open()

        else:
            er = Error('Complete todos los campos', title='Error',size_hint=(None,None),size=(600,200))
            er.open()

class MenuPrincipal(Popup):
    def __init__(self,**kwargs):
        super(MenuPrincipal,self).__init__(**kwargs)

    def build(self,u):
        box = BoxLayout(orientation='vertical')
        txt = Label(text='Menu Principal')
        gLayout = GridLayout(cols=1)
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
        self.pop = Popup(title ='Menu Principal',content=box)
        self.pop.open()

    def mostrarMaterias(self,u):
        mm = MostrarMaterias()
        mm.build(u)

    def agregarMateria(self,u):
        ss= SeleccionarMateria()
        ss.build(u)

    def cerrar(self):
        log = loginPopup()
        log.build()

class registroPop(Popup):

    def __init__(self,**kwargs):
        super(registroPop,self).__init__(**kwargs)

    def build(self):
        box= BoxLayout(orientation='vertical')
        gLayout= GridLayout(cols=2)
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
        self.pop= Popup(title='Registro', content=box)
        self.pop.open()

    def validarUsuario(self,leg,nom,app,mail,cont1,cont2):
        if (4<len(leg)<6 and 5<len(cont1) and 5<len(cont2)):
            if (leg !='' and nom!='' and app!='' and mail!='' and cont1!='' and cont2!='' and ('@' in mail and '.' in mail)):
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
                er1= Error('Complete todos los campos de manera correcta', title='Error',size_hint=(None,None),size=(600,200))
                er1.open()
        else: 
            er2=Error('Legajo y/o Password no tiene la longitud necesaria', title='Error',size_hint=(None,None),size=(600,200))
            er2.open()
   
class SeleccionarMateria(Popup):
    def __init__(self,**kwargs):
        super(SeleccionarMateria,self).__init__(**kwargs)

    def build(self,u):

        box=BoxLayout(orientation='vertical')
        txt = Label(text ='MATERIAS')
        gLayout = GridLayout(cols=2)
        m =Materia()
        mats = m.traerMaterias()
        buttons=[Button(text=mat.nombreMateria) for mat in mats]
        for button in buttons:
            button.bind(on_release= lambda button:  self.selecCom(button.text,u))
            gLayout.add_widget(button)
        btnAtras=Button(text='Atras')
        btnAtras.bind(on_release= lambda x:  self.cerrar())
        box.add_widget(txt)
        box.add_widget(gLayout)
        box.add_widget(btnAtras)
        self.pop = Popup(title='SelecionarMateria',content=box)
        self.pop.open()

    def selecCom(self,nombre_materia,u):
        sm = SeleccionarComision()
        sm.build(nombre_materia,u)
        
    def cerrar(self):
        self.pop.dismiss()

class SeleccionarComision(Popup):
    def __init__(self,**kwargs):
        super(SeleccionarComision,self).__init__(**kwargs)

    def build(self,nombre_materia,u):
        box= BoxLayout(orientation='horizontal')
        txt=Label(text='Seleccione Comision')
        gLayout = GridLayout(cols=2)
        c= ComisionMateria()
        materia=Materia().traerMateriaPorNombre(nombre_materia)
        comisiones = c.traerComisiones(materia)
        buttons=[Button(text=comision.nroComision) for comision in comisiones]
        for button in buttons:
            button.bind(on_release= lambda button:  self.confirmar(nombre_materia,button.text,u))
            gLayout.add_widget(button)
        box.add_widget(txt)
        box.add_widget(gLayout)
        self.pop = Popup(title='Seleccionar Materia',content=box)
        self.pop.open()


    def confirmar(self,nombre_materia,numero_comision,u):
        box= BoxLayout(orientation='vertical')
        txt= Label(text='¿Desea inscribirse a {materia} en la comision {comision}?'.format(materia=nombre_materia,comision=numero_comision))
        gLayout= GridLayout(cols=2)
        btnCancelar=Button(text='Cancelar')
        btnCancelar.bind(on_release= lambda x:  self.build(nombre_materia,u))#funcion boton cancelar
        btnAceptar=Button(text='Aceptar')
        btnAceptar.bind(on_release= lambda x:  self.altaACM(nombre_materia,numero_comision,u))#funcion boton aceptar
        box.add_widget(txt)
        gLayout.add_widget(btnCancelar)
        gLayout.add_widget(btnAceptar)
        box.add_widget(gLayout)
        self.pop=Popup(title='Confirmar',content=box)
        self.pop.open()
    
    def altaACM(self,nombre_materia,numero_comision,u):
        materia= Materia().traerMateriaPorNombre(nombre_materia)
        comision= Comision().traerComisionPorNumero(numero_comision)
        icm = ComisionMateria()
        cm = icm.devolver(materia,comision)
        iacm = AlumnoComisionMateria()
        res = iacm.alta(cm,u)
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