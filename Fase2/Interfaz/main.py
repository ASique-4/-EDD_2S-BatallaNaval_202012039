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
    sg.theme('DarkTeal2')
    layout = []
    botones = []
    #Numero de barcos
    constante = int(((tamanio - 1)/10)+1)
    Portaaviones = 1*constante
    Submarino = 2*constante
    Destructor = 3*constante
    Buque = 4*constante
    layout.append(
        [sg.OptionMenu(('Portaaviones', 'Submarino', 'Destructor', 'Buque'),'Portaaviones'),
        sg.Text('Portaaviones',text_color='#C98474'),sg.Text(str(Portaaviones),text_color='#C98474'),
        sg.Text('Submarino',text_color='#25316D'),sg.Text(str(Submarino),text_color='#25316D'),
        sg.Text('Destructor',text_color='#A2B5BB'),sg.Text(str(Destructor),text_color='#A2B5BB'),
        sg.Text('Buque',text_color='#6FEDD6'),sg.Text(str(Buque),text_color='#6FEDD6')
        ]
        )
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
                        if(layout[i][j].ButtonText == event and layout[i][j].ButtonColor[1] == '#394a6d'):
                            if(colorear_botones(values[0], int(i), int(j), matriz, layout)):
                                while True:
                                    event2, values = window.read()
                                    if event2 == sg.WIN_CLOSED or event2 == 'Salir':
                                        break
                                    else:
                                        for k in range(1 , len(layout)):
                                            for l in range(len(layout) - 1):
                                                if(layout[k][l].ButtonText == event2 ):
                                                    if(layout[k][l].ButtonColor[1] == '#EEF1FF'):
                                                        if values[0] == 'Portaaviones' and Portaaviones > 0:
                                                            if(pintar_portaavion(int(i), int(j), int(k), int(l), matriz, layout) != False):
                                                                limpiar_botones(layout)
                                                                Portaaviones -= 1
                                                                layout[0][2].update(Portaaviones)
                                                                break
                                                            else:
                                                                sg.PopupError("No se puede colocar el barco en esa posición", title="Error")
                                                                limpiar_botones(layout)
                                                                break
                                                        elif values[0] == 'Submarino' and Submarino > 0:
                                                            if(pintar_submarino(int(i), int(j), int(k), int(l), matriz, layout) != False):
                                                                limpiar_botones(layout)
                                                                Submarino -= 1
                                                                layout[0][4].update(Submarino)
                                                                break
                                                            else:
                                                                sg.PopupError("No se puede colocar el barco en esa posición", title="Error")
                                                                limpiar_botones(layout)
                                                                break
                                                        elif values[0] == 'Destructor' and Destructor > 0:
                                                            if(pintar_destructor(int(i), int(j), int(k), int(l), matriz, layout) != False):
                                                                limpiar_botones(layout)
                                                                Destructor -= 1
                                                                layout[0][6].update(Destructor)
                                                                break
                                                            else:
                                                                sg.PopupError("No se puede colocar el barco en esa posición", title="Error")
                                                                limpiar_botones(layout)
                                                                break
                                                        elif values[0] == 'Buque' and Buque > 0:
                                                            if(pintar_buque(int(i), int(j), int(k), int(l), matriz, layout) != False):
                                                                limpiar_botones(layout)
                                                                Buque -= 1
                                                                layout[0][8].update(Buque)
                                                                break
                                                            else:
                                                                sg.PopupError("No se puede colocar el barco en esa posición", title="Error")
                                                                limpiar_botones(layout)
                                                                break
                                                        else:
                                                            sg.popup_error('No quedan ' + values[0], title="Error")
                                                            limpiar_botones(layout)
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
    if(x2 == x1+3):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.getNodo(j, y1).caracter = "P"
            layout[j][y1].update(button_color=('black', '#C98474'))
            j += 1
    #Arriba
    elif(x2 == x1-3):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.getNodo(j, y1).caracter = "P"
            layout[j][y1].update(button_color=('black', '#C98474'))
            j -= 1
    #Derecha
    elif(y2 == y1+3):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "P"
            layout[x1][j].update(button_color=('black', '#C98474'))
            j += 1
    #Izquierda
    elif(y2 == y1-3):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.getNodo(x1, j).caracter = "P"
            layout[x1][j].update(button_color=('black', '#C98474'))
            j -= 1
    else:
        return False
#Pintar submarino
def pintar_submarino(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 2):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.getNodo(j, y1).caracter = "S"
            layout[j][y1].update(button_color=('black', '#25316D'))
            j += 1
    #Arriba
    elif(x2 == x1 - 2):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.getNodo(j, y1).caracter = "S"
            layout[j][y1].update(button_color=('black', '#25316D'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "S"
            layout[x1][j].update(button_color=('black', '#25316D'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 2):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.getNodo(x1, j).caracter = "S"
            layout[x1][j].update(button_color=('black', '#25316D'))
            j -= 1
    else:
        return False
#Pintar destructor
def pintar_destructor(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 1):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.getNodo(j, y1).caracter = "D"
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Arriba
    elif(x2 == x1 - 1):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.getNodo(j, y1).caracter = "D"
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 1):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.getNodo(x1, j).caracter = "D"
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 1):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.getNodo(x1, j).caracter = "D"
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j -= 1
    else:
        return False
#Pintar buque
def pintar_buque(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    if(x1 == x2 and y1 == y2):
        matriz.getNodo(x1, y1).caracter = "B"
        layout[x1][y1].update(button_color=('black', '#6FEDD6'))


#Limpiar botones
def limpiar_botones(layout):
    for i in range(1 , len(layout)):
        for j in range(len(layout) - 1):
            if(layout[i][j].ButtonColor[1] == '#EEF1FF'):
                layout[i][j].update(button_color=('#c0ffb3', '#394a6d'))

#No está pintado
def no_pintado(x1 :int, y1 :int, x2 :int, y2 :int, layout):
        if(x1 == x2):
            if(y1 < y2):
                for i in range(y1, y2 + 1):
                    if(layout[x1][i].ButtonColor[1] != '#394a6d'):
                        return False
            elif(y1 > y2):
                for i in range(y2, y1 - 1):
                    if(layout[x1][i].ButtonColor[1] != '#394a6d'):
                        return False
            elif(y1 == y2):
                if(layout[x1][y1].ButtonColor[1] != '#394a6d'):
                    return False
        elif(y1 == y2):
            if(x1 < x2):
                for i in range(x1, x2 + 1):
                    if(layout[i][y1].ButtonColor[1] != '#394a6d'):
                        return False
            elif(x1 > x2):
                j = x1
                for i in range(x2, x1 + 1):
                    if(layout[j][y1].ButtonColor[1] != '#394a6d'):
                        return False
                    j -= 1
            elif(x1 == x2):
                if(layout[x1][y1].ButtonColor[1] != '#394a6d'):
                    return False
        return True

#Colorear botones
def colorear_botones(barco :string, x :int, y :int, matriz :MatrizDispersa, layout):
    pintado = False
    if(barco == "Portaaviones"):
        #Abajo
        try:
            if(matriz.getNodo(x+3,y) != None and no_pintado(x, y, x + 3, y, layout)):
                for i in range(x, x + 4):
                    matriz.getNodo(i, y).caracter = "P"
                    layout[i][y].update(button_color=('black', '#EEF1FF')) 
                pintado = True
        except: 
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-4,y) != None and no_pintado(x-1, y, x - 3, y, layout)):
                j = x
                for i in range(x, x + 4):
                    matriz.getNodo(j, y).caracter = "P"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+3) != None and no_pintado(x, y+1, x, y + 3, layout)):
                j = y
                for i in range(y, y + 4):
                    matriz.getNodo(x, j).caracter = "P"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-3) != None and no_pintado(x, y+1, x, y - 3, layout)):
                j = y
                for i in range(y, y + 4):
                    matriz.getNodo(x, j).caracter = "P"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Submarino"):
        #Abajo
        try:
            if(matriz.getNodo(x+2,y) != None and no_pintado(x, y, x + 2, y, layout)):
                for i in range(x, x + 3):
                    matriz.getNodo(i, y).caracter = "S"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
                pintado = True
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-3,y) != None and no_pintado(x-1, y, x - 2, y, layout)):
                j = x
                for i in range(x, x + 3):
                    matriz.getNodo(j, y).caracter = "S"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+2) != None and no_pintado(x, y+1, x, y + 2, layout)):
                j = y
                for i in range(y, y + 3):
                    matriz.getNodo(x, j).caracter = "S"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-2) != None and no_pintado(x, y + 1, x, y - 2, layout)):
                j = y
                for i in range(y, y + 3):
                    matriz.getNodo(x, j).caracter = "S"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Destructor"):
        #Abajo
        try:
            if(matriz.getNodo(x+1,y) != None and no_pintado(x, y, x + 1, y, layout)):
                for i in range(x, x + 2):
                    matriz.getNodo(i, y).caracter = "D"
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
                pintado = True
        except:
            pass
        #Arriba
        try:
            if(matriz.getNodo(x-2,y) != None and no_pintado(x-1, y, x - 1, y, layout)):
                j = x
                for i in range(x, x + 2):
                    matriz.getNodo(j, y).caracter = "D"
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(matriz.getNodo(x,y+1) != None and no_pintado(x, y+1, x, y + 1, layout)):
                j = y
                for i in range(y, y + 2):
                    matriz.getNodo(x, j).caracter = "D"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if(matriz.getNodo(x,y-1) != None and no_pintado(x, y+1, x, y - 1, layout)):
                j = y
                for i in range(y, y + 2):
                    matriz.getNodo(x, j).caracter = "D"
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Buque"):
        try:
            if(matriz.getNodo(x,y) != None and layout[x][y].ButtonColor[1] == '#394a6d'):
                matriz.getNodo(x, y).caracter = "B"
                layout[x][y].update(button_color=('black', '#EEF1FF'))
                pintado = True
        except:
            pass
    return pintado

#Iniciar juego
def iniciar_juego():
    layout = [[sg.Text('Iniciar Juego',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Crear Tablero',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
    ]
    window = sg.Window('Iniciar juego', layout, size=(400, 300), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Regresar al menu':
            window.close()
            break
        elif event == 'Crear Tablero':
            window.close()
            crear_tablero(int(sg.popup_get_text('Ingrese el tamaño de la tablero', title='Crear Tablero', size=(5, 1))))
            break

#Tienda
def tienda():
    try:
        res = requests.get(f'{base_url}ObtenerTienda/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        layout = [[sg.Text('Tienda',size = (20,1), font="Arial 15 bold")],
                [sg.Text('Monedas: ' + str(usuario_global['monedas']),size = (20,1), font="Arial 15 bold")],
                [sg.Button('Comprar barcos',size = (20,1), font="Arial 15 bold")],
                [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
        ]
        window = sg.Window('Tienda', layout, size=(400, 300), element_justification='center')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Regresar al menu':
                window.close()
                break
            elif event == 'Comprar barcos':
                window.hide()
                comprar_barcos(data)
                window.un_hide()
                break

    except:
        sg.popup('Error al conectar con el servidor', title='Error', size=(5, 1))

#Comprar barcos
def comprar_barcos(data):
    layout = [[sg.Text('Comprar barcos',size = (20,1), font="Arial 15 bold")],
            [sg.Text('Monedas: ' + str(usuario_global['monedas']),size = (20,1), font="Arial 15 bold")],
            [sg.Text('Barcos',size = (20,1), font="Arial 15 bold")],
            [sg.Text('Submarino: ' + str(data['barcos'][0]['precio']),size = (20,1), font="Arial 15 bold")],
            [sg.Text('Destructor: ' + str(data['barcos'][1]['precio']),size = (20,1), font="Arial 15 bold")],
            [sg.Text('Buque: ' + str(data['barcos'][2]['precio']),size = (20,1), font="Arial 15 bold")],
            [sg.Button('Comprar submarino',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Comprar destructor',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Comprar buque',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
    ]
    window = sg.Window('Comprar barcos', layout, size=(400, 300), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Regresar al menu':
            window.close()
            break
        elif event == 'Comprar submarino':
            if(usuario_global['monedas'] >= data['barcos'][0]['precio']):
                usuario_global['monedas'] -= data['barcos'][0]['precio']
                usuario_global['submarinos'] += 1
                window.close()
                comprar_barcos(data)
                break
            else:
                sg.popup('No tienes suficientes monedas', title='Error', size=(5, 1))
        elif event == 'Comprar destructor':
            if(usuario_global['monedas'] >= data['barcos'][1]['precio']):
                usuario_global['monedas'] -= data['barcos'][1]['precio']
                usuario_global['destructores'] += 1
                window.close()
                comprar_barcos(data)
                break
            else:
                sg.popup('No tienes suficientes monedas', title='Error', size=(5, 1))

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
                [sg.Button('Iniciar Juego', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Datos':
            window.hide()
            cargar_datos()
            window.un_hide()
        if event == 'Iniciar Sesion':
            window.close()
            login()
        if event == 'Registrar Usuario':
            window.hide()
            registrar_usuario()
            window.un_hide()
        if event == 'Editar Usuario':
            window.hide()
            editar_usuario()
            window.un_hide()
        if event == 'Eliminar Usuario':
            
            if sg.popup_yes_no('¿Estas seguro de eliminar tu usuario?'):
                print(eliminar_usuario(usuario_global['nick'], usuario_global['password']))
                print('Eliminar usuario')
        if event == 'Iniciar Juego':
            window.hide()
            iniciar_juego()
            window.un_hide()
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
                [sg.Button('Iniciar Juego', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Datos':
            window.hide()
            cargar_datos()
            window.un_hide()
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
            window.hide()
            menu_reportes()
            window.un_hide()
        if event == 'Iniciar Juego':
            window.hide()
            iniciar_juego()
            window.un_hide()
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
    sg.theme('DarkTeal2')

    img = Image.open('/home/angel/Desktop/Dev/Github/EDD/Proyecto1/Fase2/Interfaz/login.png')    
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
        [sg.Button('Ingresar', font=letter_2, size=(27,0),pad=(0,20))],]
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
            



login()
#crear_tablero(11)
