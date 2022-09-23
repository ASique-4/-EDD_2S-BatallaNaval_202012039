import requests
import json
import PySimpleGUI as sg
from PIL import Image
import io
from MatrizDispersa import MatrizDispersa


base_url = "http://localhost:8080/"

usuario_global = {
    'nick': '',
    'password': '',
    'monedas': '',
    'edad': ''
}

#Crear tablero
def crear_tablero(ancho :int ,alto :int):
    matriz = MatrizDispersa()
    for i in range(0, (ancho)):
        for j in range(0, (alto)):
            matriz.insertar(i, j, str(i) + "," + str(j))
    matriz.graficarNeato("Tablero")


#Ruta relativa
def ruta_relativa(ruta):
    return ruta.split('/')[-1]

#verificar el inicio de sesion
def verify_login( nick,  password):
    try:
        progress_bar()
        res = requests.get(f'{base_url}ObtenerUsuario/' + nick + '/' + password + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        usuario_global['nick'] = data['usuario'][0]['nick']
        usuario_global['password'] = data['usuario'][0]['password']
        usuario_global['monedas'] = data['usuario'][0]['monedas']
        usuario_global['edad'] = data['usuario'][0]['edad']
        return (data['status'])

    except:
        return "error"

#Menu
def menu():
    layout = [[sg.Text('Menu',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Cargar Datos', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Crear Tablero', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Iniciar Sesion', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Registrar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Editar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Eliminar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Datos':
            cargar_datos()
        if event == 'Iniciar Sesion':
            login()
        if event == 'Registrar Usuario':
            registrar_usuario()
        if event == 'Editar Usuario':
            editar_usuario()
        if event == 'Eliminar Usuario':
            
            if sg.popup_yes_no('¿Estas seguro de eliminar tu usuario?'):
                print(eliminar_usuario(usuario_global['nick'], usuario_global['password']))
                print('Eliminar usuario')
            
    window.close()
    return event

#Eliminar Usuario
def eliminar_usuario(nick, password):
    try:
        progress_bar()
        print(nick, password)
        res = requests.get(f'{base_url}EliminarUsuario/' + nick + '/' + password + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        return (data['status'])
    except:
        return "error"

#Crear tablero


#Registrar usuario
def registrar_usuario():
    layout = [[sg.Text('Registrar Usuario',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Text('Nick',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Password',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Edad',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Button('Registrar', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Registrar':
            registrar(values[0], values[1], values[2])
    window.close()
    return event

#Registrar
def registrar(nick, password, edad):
    try:
        progress_bar()
        res = requests.get(f'{base_url}CrearUsuario/' + nick + '/' + password + '/' + edad + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return (data['status'])
    except:
        return "error"

#Editar usuario
def editar_usuario():
    layout = [[sg.Text('Editar Usuario',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Text('Nick',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Password',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Edad',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Button('Editar', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Editar':
            editar(values[0], values[1], values[2])
    window.close()
    return event

#Editar
def editar(nick, password, edad):
    try:
        progress_bar()
        if(nick != "" & password == "" & edad == ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + nick + '/' + usuario_global['password'] + '/' + usuario_global['edad'] + '/')
        elif (nick == "" & password != "" & edad == ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['nick'] + '/' + password + '/' + usuario_global['edad'] + '/')
        elif (nick == "" & password == "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['nick'] + '/' + usuario_global['password'] + '/' + edad + '/')
        elif (nick == "" & password != "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['nick'] + '/' + password + '/' + edad + '/')
        elif (nick != "" & password == "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + nick + '/' + usuario_global['password'] + '/' + edad + '/')
        elif (nick != "" & password != "" & edad == ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + nick + '/' + password + '/' + usuario_global['edad'] + '/')
        else:
            res = requests.get(f'{base_url}ModificarUsuario/' + nick + '/' + password + '/' + edad + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return (data['status'])
    except:
        return "error"


#Cargar datos
def cargar_datos():
    layout = [[sg.Text('Cargar Datos',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Cargar Archivo', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            print(values)
            break
        if event == 'Cargar Archivo':
            
            cargar_archivo(sg.popup_get_file('Cargar Archivo', no_window=True, file_types=(("JSON Files", "*.json"),)))
    window.close()
    return event

#Cargar archivo
def cargar_archivo(archivo):
    try:
        print(ruta_relativa(archivo))
        res = requests.post(f'{base_url}Cargar/' + ruta_relativa(archivo))
        res = requests.get(f'{base_url}Cargar/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return (data['status'])
    except:
        return "error"

#Menu Admin
def menu_admin():
    layout = [[sg.Text('Menu De Administrador',size = (20,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Cargar Datos', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Iniciar Sesion', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Registrar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Editar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Eliminar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Datos':
            window.hide()
            cargar_datos()
        if event == 'Iniciar Sesion':
            window.close()
            login()
        if event == 'Registrar Usuario':
            registrar_usuario()
        if event == 'Editar Usuario':
            editar_usuario()
        if event == 'Eliminar Usuario':
            eliminar_usuario(usuario_global['nick'],usuario_global['password'])
        if event == 'Reportes':
            menu_reportes()

    window.close()
    return event

#Menu Reportes
def menu_reportes():
    layout = [[sg.Text('Reportes',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Reportes de usuarios', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de articulos', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de tutorial', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    event, values = window.read()
    window.close()
    return event

#Menu Reportes de usuarios
def menu_reportes_usuarios():
    layout = [[sg.Text('Reportes de usuarios',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Ordenar de manera ascendente', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Ordenar de manera descendente', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    event, values = window.read()
    window.close()
    return event

#Menu Reportes de articulos
def menu_reportes_articulos():
    layout = [[sg.Text('Reportes de articulos',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Ordenar de manera ascendente', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Ordenar de manera descendente', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    event, values = window.read()
    window.close()
    return event

#ProgressBar
def progress_bar():
    # layout the window
    layout = [[sg.Text('Buscando usuario...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
            [sg.Cancel()]]

    # create the window`
    window = sg.Window('Cargando...', layout)
    progress_bar = window['progressbar']
    # loop that would normally do something useful
    for i in range(1000):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=1.75)
        if event == 'Cancel'  or event == sg.WIN_CLOSED:
            break
    # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.UpdateBar(i + 1)
    # done with loop... need to destroy the window as it's still open
    window.close()

#Create the login interface
def login():
    sg.theme('BlueMono')

    img = Image.open('/home/angel/Desktop/Dev/Github/EDD/Proyecto1/Fase2/Frontend/login.png')    
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    data = bio.getvalue()
    letter = "Arial 30 bold"
    letter_2 = "Arial 12 bold"
    letter_3 = "Arial 12"
    layout = [
        [sg.Text('Login',size = (10,0), font=letter, justification='center')],
        [sg.Image(data=data)],
        [sg.Text('Usuario', font=letter_2,pad=(0,10),justification='left')],
        [sg.Input(size=(29,0),font=letter_3)],
        [sg.Text('Contraseña', font=letter_2,pad=(0,10),justification='left')],
        [sg.Input(size=(29,0),pad=(0,10),password_char='*', font=letter_3)],
        [sg.Button('Ingresar', font=letter_2, size=(27,0),pad=(0,20))]]
    window = sg.Window('Login', layout,size=(300, 550), element_justification='center',finalize=True)
    
    while True:
        event, values = window.read()
        #veficar el inicio de sesion
        if (verify_login(values[1],values[2])) == "ok":
            window.close()
            if(values[1] == "EDD"):
                menu_admin()
            else:
                menu()
        elif event == sg.WIN_CLOSED:
            window.close()
        else:
            sg.PopupError('Usuario o contraseña incorrectos', title='Error')
            
    window.close()



#login()
crear_tablero(10,10)