import string
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
def crear_tablero(tamanio :int):
    layout = []
    botones = []
    layout.append([sg.OptionMenu(('Portaaviones', 'Submarino', 'Destructor', 'Buque'),'Portaaviones')])
    #Si el ancho y alto es mayor a 10
    if(tamanio >= 10):
        matriz = MatrizDispersa()
        for i in range(0, (tamanio) + 1):
            #Si los botones no están vacios los limpia
            if(len(botones) > 0):
                layout.append(botones)
                botones = []
                
            for j in range(0, (tamanio)):
                matriz.insertar(i, j, str(i) + "," + str(j))
                boton = sg.Button(str(i) + "," + str(j), size = (4,1), font="Arial 8 bold")
                botones.append(boton)
        matriz.graficarNeato("Tablero")

        #Colocar barcos
        img = Image.open('matriz_Tablero.png')    
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        window =  sg.Window('Menu', layout, element_justification='c')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Salir':
                break
            else:
                for i in range(1 , len(layout)):
                    for j in range(len(layout) - 1):
                        if(layout[i][j].ButtonText == event):
                            colorear_botones(values[0], int(i), int(j), matriz, layout)
                
                            while True:
                                event2, values = window.read()
                                if event2 == sg.WIN_CLOSED or event2 == 'Salir':
                                    break
                                else:
                                    for k in range(1 , len(layout)):
                                        for l in range(len(layout) - 1):
                                            if(layout[k][l].ButtonText == event2 ):
                                                if(layout[k][l].ButtonColor[1] == '#EEF1FF'):
                                                    if values[0] == 'Portaaviones':
                                                        pintar_portaavion(int(i), int(j), int(k), int(l), matriz, layout)
                                                        limpiar_botones(layout)
                                                        break
                                                    elif values[0] == 'Submarino':
                                                        pintar_submarino(int(i), int(j), int(k), int(l), matriz, layout)
                                                        limpiar_botones(layout)
                                                        break
                                                    elif values[0] == 'Destructor':
                                                        pintar_destructor(int(i), int(j), int(k), int(l), matriz, layout)
                                                        limpiar_botones(layout)
                                                        break
                                                    elif values[0] == 'Buque':
                                                        pintar_buque(int(i), int(j), int(k), int(l), matriz, layout)
                                                        limpiar_botones(layout)
                                                        break
                                                else:
                                                    sg.PopupError("No se puede colocar el barco en esa posición", title="Error")
                                                    limpiar_botones(layout)
                                                    break
                                                break
                                    break
                            break

                                            

             
    else:
        sg.PopupError("El alto y ancho debe ser mayor a 10", title="Error")

#Pintar portaavion
def pintar_portaavion(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x1 < x2):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.getNodo(j, y1).caracter = "P"
            layout[j][y1].update(button_color=('black', '#FFE9A0'))
            j += 1
    #Arriba
    elif(x1 > x2):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.getNodo(j, y1).caracter = "P"
            layout[j][y1].update(button_color=('black', '#FFE9A0'))
            j -= 1
    #Derecha
    elif(y1 < y2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "P"
            layout[x1][j].update(button_color=('black', '#FFE9A0'))
            j += 1
    #Izquierda
    elif(y1 > y2):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.getNodo(x1, j).caracter = "P"
            layout[x1][j].update(button_color=('black', '#FFE9A0'))
            j -= 1

#Pintar submarino
def pintar_submarino(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x1 < x2):
        for i in range(x1, x2 + 1):
            matriz.getNodo(i, y1).caracter = "S"
            layout[i][y1].update(button_color=('black', '#367E18'))
    #Arriba
    elif(x1 > x2):
        j = x1
        for i in range(x1, x2 - 1):
            matriz.getNodo(j, y1).caracter = "S"
            layout[j][y1].update(button_color=('black', '#367E18'))
            j -= 1
    #Derecha
    elif(y1 < y2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "S"
            layout[x1][j].update(button_color=('black', '#367E18'))
            j += 1
    #Izquierda
    elif(y1 > y2):
        j = y1
        for i in range(y1, y2 - 1):
            matriz.getNodo(x1, j).caracter = "S"
            layout[x1][j].update(button_color=('black', '#367E18'))
            j -= 1

#Pintar destructor
def pintar_destructor(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x1 < x2):
        for i in range(x1, x2 + 1):
            matriz.getNodo(i, y1).caracter = "D"
            layout[i][y1].update(button_color=('black', '#F57328'))
    #Arriba
    elif(x1 > x2):
        j = x1
        for i in range(x1, x2 - 1):
            matriz.getNodo(j, y1).caracter = "D"
            layout[j][y1].update(button_color=('black', '#F57328'))
            j -= 1
    #Derecha
    elif(y1 < y2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "D"
            layout[x1][j].update(button_color=('black', '#F57328'))
            j += 1
    #Izquierda
    elif(y1 > y2):
        j = y1
        for i in range(y1, y2 - 1):
            matriz.getNodo(x1, j).caracter = "D"
            layout[x1][j].update(button_color=('black', '#F57328'))
            j -= 1

#Pintar buque
def pintar_buque(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x1 < x2):
        for i in range(x1, x2 + 1):
            matriz.getNodo(i, y1).caracter = "B"
            layout[i][y1].update(button_color=('black', '#CC3636'))
    #Arriba
    elif(x1 > x2):
        j = x1
        for i in range(x1, x2 - 1):
            matriz.getNodo(j, y1).caracter = "B"
            layout[j][y1].update(button_color=('black', '#CC3636'))
            j -= 1
    #Derecha
    elif(y1 < y2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "B"
            layout[x1][j].update(button_color=('black', '#CC3636'))
            j += 1
    #Izquierda
    elif(y1 > y2):
        j = y1
        for i in range(y1, y2 - 1):
            matriz.getNodo(x1, j).caracter = "B"
            layout[x1][j].update(button_color=('black', '#CC3636'))
            j -= 1

#Limpiar botones
def limpiar_botones(layout):
    for i in range(1 , len(layout)):
        for j in range(len(layout) - 1):
            if(layout[i][j].ButtonColor[1] == '#EEF1FF'):
                layout[i][j].update(button_color=('#FFFFFF', '#283b5b'))

#Colorear botones
def colorear_botones(barco :string, x :int, y :int, matriz :MatrizDispersa, layout):
    if(barco == "Portaaviones"):
        #Abajo
        try:
            if(matriz.getNodo(x+3,y) != None):
                for i in range(x, x + 4):
                    matriz.getNodo(i, y).caracter = "P"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-3,y) != None):
                j = x
                for i in range(x, x + 4):
                    matriz.getNodo(j, y).caracter = "P"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+3) != None):
                j = y
                for i in range(y, y + 4):
                    matriz.getNodo(x, j).caracter = "P"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-3) != None):
                j = y
                for i in range(y, y + 4):
                    matriz.getNodo(x, j).caracter = "P"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            print(j)
            print("Error")
            pass
    elif(barco == "Submarino"):
        #Abajo
        try:
            if(matriz.getNodo(x+2,y) != None):
                for i in range(x, x + 3):
                    matriz.getNodo(i, y).caracter = "S"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-2,y) != None):
                j = x
                for i in range(x, x + 3):
                    matriz.getNodo(j, y).caracter = "S"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    
                    j -= 1
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+2) != None):
                j = y
                for i in range(y, y + 3):
                    matriz.getNodo(x, j).caracter = "S"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-2) != None):
                j = y
                for i in range(y, y + 3):
                    matriz.getNodo(x, j).caracter = "S"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass
    elif(barco == "Destructor"):
        #Abajo
        try:
            if(matriz.getNodo(x+1,y) != None):
                for i in range(x, x + 2):
                    matriz.getNodo(i, y).caracter = "D"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-1,y) != None):
                j = x
                for i in range(x, x + 2):
                    matriz.getNodo(j, y).caracter = "D"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+1) != None):
                j = y
                for i in range(y, y + 2):
                    matriz.getNodo(x, j).caracter = "D"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-1) != None):
                j = y
                for i in range(y, y + 2):
                    matriz.getNodo(x, j).caracter = "D"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass
    elif(barco == "Buque"):
        #Abajo
        try:
            if(matriz.getNodo(x,y) != None):
                for i in range(x, x + 1):
                    matriz.getNodo(i, y).caracter = "B"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x,y) != None):
                j = x
                for i in range(x, x + 1):
                    matriz.getNodo(j, y).caracter = "B"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y) != None):
                j = y
                for i in range(y, y + 1):
                    matriz.getNodo(x, j).caracter = "B"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y) != None):
                j = y
                for i in range(y, y + 1):
                    matriz.getNodo(x, j).caracter = "B"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
        except:
            pass


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
            window.close()
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
            



#login()
crear_tablero(10)
