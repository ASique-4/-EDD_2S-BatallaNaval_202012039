import string
import webbrowser
import requests
import json
import PySimpleGUI as sg
from MatrizDispersa import MatrizDispersa


base_url = "http://localhost:8080/"

usuario_global = {
    'nick': '',
    'password': '',
    'monedas': '1000',
    'edad': '',
    'id': ''
}

usuarios = []



#Crear tablero
def crear_tablero(tamanio :int):
    sg.theme('DarkTeal4')
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
                boton = sg.Button(str(i) + "," + str(j), size = (4,1), font="Arial 8 bold")
                botones.append(boton)
        

        #Colocar barcos
        window =  sg.Window('Menu', layout, element_justification='c')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Salir':
                matriz.graficarNeato('Tablero')
                break
            else:
                for i in range(1 , len(layout)):
                    for j in range(len(layout) - 1):
                        if(layout[i][j].ButtonText == event and layout[i][j].ButtonColor[1] == '#6c7b95'):
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
            matriz.insertar(j-1, y1, "P")
            layout[j][y1].update(button_color=('black', '#C98474'))
            j += 1
    #Arriba
    elif(x2 == x1-3):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "P")
            layout[j][y1].update(button_color=('black', '#C98474'))
            j -= 1
    #Derecha
    elif(y2 == y1+3):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1, j, "P")
            layout[x1][j].update(button_color=('black', '#C98474'))
            j += 1
    #Izquierda
    elif(y2 == y1-3):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1, j, "P")
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
            matriz.insertar(j, y1, "S")
            layout[j][y1].update(button_color=('black', '#25316D'))
            j += 1
    #Arriba
    elif(x2 == x1 - 2):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j, y1, "S")
            layout[j][y1].update(button_color=('black', '#25316D'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1, j, "S")
            layout[x1][j].update(button_color=('black', '#25316D'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 2):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1, j, "S")
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
            matriz.insertar(j, y1, "D")
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Arriba
    elif(x2 == x1 - 1):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j, y1, "D")
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 1):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1, j, "D")
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 1):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1, j, "D")
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j -= 1
    else:
        return False
#Pintar buque
def pintar_buque(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    if(x1 == x2 and y1 == y2):
        matriz.insertar(x1, y1, "B")
        layout[x1][y1].update(button_color=('black', '#6FEDD6'))


#Limpiar botones
def limpiar_botones(layout):
    for i in range(1 , len(layout)):
        for j in range(len(layout) - 1):
            if(layout[i][j].ButtonColor[1] == '#EEF1FF'):
                layout[i][j].update(button_color=('#FFFFFF', '#6c7b95'))

#No está pintado
def no_pintado(x1 :int, y1 :int, x2 :int, y2 :int, layout):
        if(x1 == x2):
            if(y1 < y2):
                for i in range(y1, y2 + 1):
                    if(layout[x1][i].ButtonColor[1] != '#6c7b95'):
                        return False
            elif(y1 > y2):
                for i in range(y2, y1 - 1):
                    if(layout[x1][i].ButtonColor[1] != '#6c7b95'):
                        return False
            elif(y1 == y2):
                if(layout[x1][y1].ButtonColor[1] != '#6c7b95'):
                    return False
        elif(y1 == y2):
            if(x1 < x2):
                for i in range(x1, x2 + 1):
                    if(layout[i][y1].ButtonColor[1] != '#6c7b95'):
                        return False
            elif(x1 > x2):
                j = x1
                for i in range(x2, x1 + 1):
                    if(layout[j][y1].ButtonColor[1] != '#6c7b95'):
                        return False
                    j -= 1
            elif(x1 == x2):
                if(layout[x1][y1].ButtonColor[1] != '#6c7b95'):
                    return False
        return True

#Colorear botones
def colorear_botones(barco :string, x :int, y :int, matriz :MatrizDispersa, layout):
    pintado = False
    if(barco == "Portaaviones"):
        #Abajo
        try:
            if(no_pintado(x, y, x + 3, y, layout)):
                for i in range(x, x + 4):
                    layout[i][y].update(button_color=('black', '#EEF1FF')) 
                pintado = True
        except: 
            pass
        #Arriba
        try:
            if(no_pintado(x-1, y, x - 3, y, layout)):
                j = x
                for i in range(x, x + 4):
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(no_pintado(x, y+1, x, y + 3, layout)):
                j = y
                for i in range(y, y + 4):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if( (y - 3) >= 0 and no_pintado(x, y+1, x, y - 3, layout)):
                j = y
                for i in range(y, y + 4):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Submarino"):
        #Abajo
        try:
            if(no_pintado(x, y, x + 2, y, layout)):
                for i in range(x, x + 3):
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
                pintado = True
        except:
            pass
        #Arriba
        try:
            if(no_pintado(x-1, y, x - 2, y, layout)):
                j = x
                for i in range(x, x + 3):
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(no_pintado(x, y+1, x, y + 2, layout)):
                j = y
                for i in range(y, y + 3):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if((y - 2) >= 0 and no_pintado(x, y + 1, x, y - 2, layout)):
                j = y
                for i in range(y, y + 3):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Destructor"):
        #Abajo
        try:
            if(no_pintado(x, y, x + 1, y, layout)):
                for i in range(x, x + 2):
                    layout[i][y].update(button_color=('black', '#EEF1FF'))
                pintado = True
        except:
            pass
        #Arriba
        try:
            if(no_pintado(x-1, y, x - 1, y, layout)):
                j = x
                for i in range(x, x + 2):
                    layout[j][y].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
        #Derecha
        try:
            if(no_pintado(x, y+1, x, y + 1, layout)):
                j = y
                for i in range(y, y + 2):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j += 1
                pintado = True
        except:
            pass
        #Izquierda
        try:
            if((y - 1) >= 0 and no_pintado(x, y+1, x, y - 1, layout)):
                j = y
                for i in range(y, y + 2):
                    layout[x][j].update(button_color=('black', '#EEF1FF'))
                    j -= 1
                pintado = True
        except:
            pass
    elif(barco == "Buque"):
        try:
            if(layout[x][y].ButtonColor[1] == '#6c7b95'):
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
    window = sg.Window('Iniciar juego', layout, size=(300, 250), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Regresar al menu':
            window.close()
            break
        elif event == 'Crear Tablero':
            window.close()
            crear_tablero(int(sg.popup_get_text('Ingrese el tamaño de la tablero', title='Crear Tablero', size=(5, 1))))
            break

#Llenar lista de articulos
def llenar_articulos(array_articulos):
    articulos = []
    for i in array_articulos[1]:
        articulos.append([i['nombre'] , (i['precio']), i['id'], i['src']])
    return articulos
    


#Tienda
def tienda():
        sg.theme('DarkTeal4')
        res = requests.get(f'{base_url}ObtenerTienda/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        categoria = []
        combo = []
        for i in data:
            categoria.append([i,data[i]])
            combo.append(i)
        articulos = llenar_articulos(categoria[0])
        layout = [[sg.Text('TIENDA',size = (20,1), font="Arial 30 bold",justification='center')],
                [sg.Text('Monedas: ' + str(usuario_global['monedas']),size = (20,1), font="Arial 15 bold",justification='center')],
                [sg.Text('Categoria',size = (20,1), font="Arial 15 bold",justification='center')],
                [sg.Combo(combo, size=(20, 5), key='categoria'), sg.Button('Buscar',size = (20,1), font="Arial 10 bold")],
                [sg.Text('Articulos',size = (20,1), font="Arial 15 bold",justification='center')],
                [sg.Table(values=articulos, headings=['Articulos','Precio','Id'], max_col_width=20, auto_size_columns=True, justification='left', num_rows=10, key='tabla')],
                [sg.Button('Comprar',size = (20,1), font="Arial 15 bold")],
                [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
        ]
        window = sg.Window('Tienda', layout, size=(600, 500), element_justification='center')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Regresar al menu':
                window.close()
                break     
            elif event == 'Buscar':
                layout[5][0].update(values=llenar_articulos(categoria[combo.index(values['categoria'])]))
                articulos = llenar_articulos(categoria[combo.index(values['categoria'])])
            elif event == 'Comprar':
                if(values['categoria'] == None):
                    sg.popup('Seleccione una categoria', title='Error')
                else:
                    window.hide()
                    #print(articulos)
                    print(articulos[values['tabla'][0]])
                    comprar_articulo(articulos[values['tabla'][0]])
                    window.un_hide()
                    
                    
            
#Agregar compra
def agregar_compra(product_id,cantidad):
    try:
        progress_bar()
        res = requests.get(f'{base_url}Comprar/' + usuario_global['nick'] + '/' + usuario_global['password'] + '/' + product_id + '/' + cantidad + '/' + cantidad + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        usuario_global['monedas'] = data['monedas']
        return data['status']
    except:
        sg.popup('No se pudo realizar la compra', title='Error')
        return 'errror'
            


#Comprar barcos
def comprar_articulo(data):
    layout = [[sg.Text('COMPRAR BARCO',size = (20,1), font="Arial 30 bold",justification='center')],
            [sg.Text('Monedas: ' + str(usuario_global['monedas']),size = (20,1), font="Arial 15 bold",justification='center')],
            [sg.Text('Nombre: ' + data[0], font="Arial 15 bold",justification='center')],
            [sg.Text('Precio: ' + str(data[1]), font="Arial 15 bold",justification='center')],
            [sg.Text('Id: ' + str(data[2]), font="Arial 15 bold",justification='center')],
            [sg.Text('Imagen: ',size = (20,1), font="Arial 15 bold",justification='center')],
            [sg.Image(data[3],background_color='#EEF1FF')],
            [sg.Text('Cantidad' ,size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText(key='cantidad',size = (10,0), font="Arial 15 bold", justification='center')],
            [sg.Button('Comprar',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
    ]
    window = sg.Window('Comprar barco', layout, size=(450, 650), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Regresar al menu':
            window.close()
            break
        elif event == 'Comprar':
            if(int(usuario_global['monedas']) < int(data[1])):
                sg.popup('No tiene suficientes monedas', title='Error')
            else:
                window.close()
                if(agregar_compra(str(data[2]),int(values['cantidad'])) == 'ok'):
                    sg.popup('Compra exitosa', title='Exito')
                    usuario_global['monedas'] = int(usuario_global['monedas']) - int(data[1])
                else:
                    sg.popup('Error al comprar', title='Error')
                break

#Ruta relativa
def ruta_relativa(ruta):
    return ruta.split('/')[-1]

#verificar el inicio de sesion
def verify_login( nick,  password):
    try:
        progress_bar()
        print(nick)
        print(password)
        print(f'{base_url}ObtenerUsuario/' + nick + '/' + password + '/' + regresar_id_usuario(nick) + '/')
        res = requests.get(f'{base_url}ObtenerUsuario/' + nick + '/' + password + '/' + regresar_id_usuario(nick) + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        usuario_global['nick'] = data['usuario'][0]['nick']
        usuario_global['password'] = data['usuario'][0]['password']
        usuario_global['monedas'] = data['usuario'][0]['monedas']
        usuario_global['edad'] = data['usuario'][0]['edad']
        usuario_global['id'] = data['usuario'][0]['id']
        return (data['status'])

    except:
        return "error"

#progress bar
def progress_bar():
    layout = [[sg.Text('Espere un momento...')],
              [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]

    window = sg.Window('Espere un momento...', layout)

    progress_bar = window['progressbar']
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        progress_bar.UpdateBar(i + 1)
    window.close()

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
                [sg.Button('Tienda', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(300, 550), element_justification='c')
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
                print(eliminar_usuario(usuario_global['id']))
                print('Eliminar usuario')
        if event == 'Iniciar Juego':
            window.hide()
            iniciar_juego()
            window.un_hide()
        if event == 'Tienda':
            window.hide()
            tienda()
            window.un_hide()
        if event == 'Reportes':
            menu_reportes()
    window.close()
    return event

#Eliminar Usuario
def eliminar_usuario(id):
    try:
        progress_bar()
        res = requests.get(f'{base_url}EliminarUsuario/' + id + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        return (data['status'])
    except:
        return "error"

#Registrar usuario
def registrar_usuario():
    layout = [[sg.Text('Registrar Usuario', font="Arial 30 bold", justification='center')],
                [sg.Text('Nick',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Password',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Text('Edad',size = (10,0), font="Arial 15 bold", justification='center'), sg.InputText()],
                [sg.Button('Registrar', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 300), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Registrar':
            registrar(values[0], values[1], values[2])
    window.close()
    return event

#Usuario existe
def usuario_existe(nick):
    for i in usuarios:
        if i[0] == nick:
            return True
    return False

#Regresar id usuario
def regresar_id_usuario(nick):
    for i in usuarios:
        if i[0] == nick:
            return i[1]
    return ''
#Registrar
def registrar(nick, password, edad):
    try:
        progress_bar()
        if (usuario_existe(nick) == False):
            res = requests.get(f'{base_url}CrearUsuario/' + nick + '/' + password + '/' + edad + '/')
            data = res.text#convertimos la respuesta en dict
            data = json.loads(data)
            usuarios.append([nick, usuarios[-1][1] + 1])
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
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + nick + '/' + usuario_global['password'] + '/' + usuario_global['edad'] + '/')
        elif (nick == "" & password != "" & edad == ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + usuario_global['nick'] + '/' + password + '/' + usuario_global['edad'] + '/')
        elif (nick == "" & password == "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + usuario_global['nick'] + '/' + usuario_global['password'] + '/' + edad + '/')
        elif (nick == "" & password != "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + usuario_global['nick'] + '/' + password + '/' + edad + '/')
        elif (nick != "" & password == "" & edad != ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + nick + '/' + usuario_global['password'] + '/' + edad + '/')
        elif (nick != "" & password != "" & edad == ""):
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + nick + '/' + password + '/' + usuario_global['edad'] + '/')
        else:
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + nick + '/' + password + '/' + edad + '/')
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
    window = sg.Window('Menu', layout, size=(300, 250), element_justification='c')
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

        for row in data['usuarios']:
            usuarios.append([row['nick'],row['id']])

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
                [sg.Button('Tienda', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(500, 550), element_justification='c')

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
            eliminar_usuario(usuario_global['id'])
        if event == 'Reportes':
            window.hide()
            menu_reportes_admin()
            window.un_hide()
        if event == 'Iniciar Juego':
            window.hide()
            iniciar_juego()
            window.un_hide()
        if event == 'Tienda':
            window.hide()
            tienda()
            window.un_hide()
    window.close()
    return event

#Menu Reportes
def menu_reportes():
    layout = [[sg.Text('Reportes',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Reportes de compras', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(300, 250), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Reportes de compras':
            window.hide()
            mostrar_reportes('compras')
            window.un_hide()
    window.close()
    return event

#Menu Reportes Admin
def menu_reportes_admin():
    layout = [[sg.Text('Reportes',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Reportes de usuarios', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de compras', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(300, 250), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Reportes de usuarios':
            window.hide()
            mostrar_reportes('arbol')
            window.un_hide()
        if event == 'Reportes de compras':
            window.hide()
            mostrar_reportes('compras')
            window.un_hide()
    window.close()
    return event

#Mostrar reportes
def mostrar_reportes(reporte):
    try:
        res = requests.get(f'{base_url}Graficar/' + reporte + '/' + usuario_global['id'] + '/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        if data['status'] == 'ok':
            sg.popup('Reporte generado')
            webbrowser.open_new_tab(data['url'])
        else:
            sg.popup('Error al generar el reporte')
    except:
        sg.popup('Error al generar el reporte')


def login():

    letter = "Arial 30 bold"
    letter_2 = "Arial 12 bold"
    letter_3 = "Arial 12"
    layout = [
        [sg.Text('Login',size = (10,0), font=letter, justification='center')],
        [sg.Image('/home/angel/Desktop/Dev/Github/EDD/Proyecto1/Fase2/Interfaz/login.png')],
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
            

#Menu principal
def menuPrincipal():
    sg.theme('DarkTeal4')

    layout = [[sg.Text('Menu',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Cargar datos', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Crear Usuarios', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Iniciar Sesion', size = (20,0), font="Arial 15 bold")]
                ]
    window = sg.Window('Menu', layout, size=(300, 250), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Cargar datos':
            window.hide()
            cargar_datos()
            window.un_hide()
        if event == 'Crear Usuarios':
            window.hide()
            registrar_usuario()
            window.un_hide()
        if event == 'Iniciar Sesion':
            window.close()
            login()
    window.close()

#login()
crear_tablero(11)
#tienda()
#menuPrincipal()
#menu()