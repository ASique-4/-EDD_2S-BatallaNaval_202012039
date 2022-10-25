import io
import os
import random
import string
import webbrowser
import json
import requests
from PIL import Image
import PySimpleGUI as sg
from MatrizDispersa import MatrizDispersa
from ListaDG import ListaDG

disparos = ListaDG()

# Creating a list of lists, where each list contains the name of a user and the number of games they
# have played.
base_url = "http://localhost:8080/"

usuario_global = {
    'nick': '',
    'password': '',
    'monedas': '1000',
    'edad': '',
    'id': '',
    'juegos': '0',
    'puntos': '0',
    'fallos': '0'
}

invitado = {
    'nick': 'Invitado',
    'password': 'Invitado',
    'monedas': '1000',
    'edad': '0',
    'id': '-1',
    'juegos': '0',
    'puntos': '0',
    'fallos': '0'
}

usuarios = [['EDD','0']]

def tablero_1vs1(tamanio :int):
    usuario_global['puntos'] = usuario_global['monedas']
    invitado['puntos'] = invitado['monedas']
    usuario_global['fallos'] = '0'
    invitado['fallos'] = '0'
    sg.theme('DarkTeal4')   # Add a touch of color
    if(tamanio >= 10):
        layout = []
        botones = []
        #Numero de barcos
        constante = int(((tamanio - 1)/10)+1)
        Portaaviones = 1*constante
        Submarino = 2*constante
        Destructor = 3*constante
        Buque = 4*constante
        vidas = 3
        layout.append(
            [
            sg.OptionMenu(('Portaaviones', 'Submarino', 'Destructor', 'Buque'),'Portaaviones',key='barco'),
            sg.Text('Vidas',text_color='#FFABE1',font='Futura 15'),sg.Text(vidas,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Puntos',text_color='#FFABE1',font='Futura 15'),sg.Text(usuario_global['monedas'],text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Portaaviones',text_color='#FFABE1',font='Futura 15'),sg.Text(Portaaviones,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Submarino',text_color='#FFABE1',font='Futura 15'),sg.Text(Submarino,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Destructor',text_color='#FFABE1',font='Futura 15'),sg.Text(Destructor,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Buque',text_color='#FFABE1',font='Futura 15'),sg.Text(Buque,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Retroceder un movimiento',button_color=('black','#FFABE1'),font='Futura 10'),
            ]
            )
        matriz = MatrizDispersa()
        matriz.nombre = '1'
        for i in range(0, (tamanio) + 1):
            #Si los botones no están vacios los limpia
            if(len(botones) > 0):
                layout.append(botones)
                botones = []
                
            for j in range(0, (tamanio)):
                boton = sg.Button(str(i) + "," + str(j), size = (4,1), font="Arial 8 bold",border_width="0")
                botones.append(boton)
        
        window =  sg.Window('Menu', layout, element_justification='c')
        sg.popup_ok('Colque sus barcos en el tablero')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                try:
                    matriz.graficarNeato('1vs1')
                except:
                    pass
                tablero_jugador2(matriz, tamanio)
                break
            elif event == 'Retroceder un movimiento':
                print('Retroceder un movimiento')
            else:
                for k in range(1 , len(layout)):
                    for l in range(len(layout) - 1):
                        if(layout[k][l].ButtonText == event and layout[k][l].ButtonColor[1] == '#6c7b95'):
                            print(values['barco'])
                            if(colorear_botones(values['barco'],k,l,matriz,layout)):
                                while True:
                                    event2, values2 = window.read()
                                    if event2 == sg.WIN_CLOSED:
                                        break
                                    else:
                                        for k2 in range(1 , len(layout)):
                                            for l2 in range(len(layout) - 1):
                                                if(layout[k2][l2].ButtonText == event2 and layout[k2][l2].ButtonColor[1] == '#EEF1FF'):
                                                    if(values['barco'] == 'Portaaviones' and portaavionesNoPintado(k,l,k2,l2,matriz)):
                                                        if(Portaaviones > 0):
                                                            print(k2,l2)
                                                            pintar_portaavion_1vs1(k,l,k2,l2,matriz,layout)
                                                            limpiar_botones(layout)
                                                            Portaaviones -= 1
                                                            layout[0][8].update(Portaaviones)
                                                            break
                                                    elif(values['barco'] == 'Submarino' and submarinoNoPintado(k,l,k2,l2,matriz)):
                                                        if(Submarino > 0):
                                                            print(k2,l2)
                                                            pintar_submarino_1vs1(k,l,k2,l2,matriz,layout)
                                                            limpiar_botones(layout)
                                                            Submarino -= 1
                                                            layout[0][11].update(Submarino)
                                                            break
                                                    elif(values['barco'] == 'Destructor' and destructorNoPintado(k,l,k2,l2,matriz)):
                                                        if(Destructor > 0):
                                                            print(k2,l2)
                                                            pintar_destructor_1vs1(k,l,k2,l2,matriz,layout)
                                                            limpiar_botones(layout)
                                                            Destructor -= 1
                                                            layout[0][14].update(Destructor)
                                                            break
                                                    elif(values['barco'] == 'Buque'):
                                                        if(Buque > 0):
                                                            print(k2,l2)
                                                            pintar_buque_1vs1(k,l,k2,l2,matriz,layout)
                                                            limpiar_botones(layout)
                                                            Buque -= 1
                                                            layout[0][17].update(Buque)
                                                            break
                                                    limpiar_botones(layout)
                                    break
                                break
                        
                    
#Tablero jugador 2
def tablero_jugador2(matriz :MatrizDispersa, tamanio :int):
    sg.theme('DarkTeal4')
    vidas = 3
    Errores = 0
    puntos = 0
    botones = []
    layout = []
    layout.append(
            [
            sg.Text('Puntos del jugador 2: ',text_color='#FFABE1',font='Futura 15'),sg.Text(invitado['monedas'],text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Retroceder un movimiento',button_color=('black','#FFABE1'),font='Futura 10'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Jugador 2 atacando',text_color='#FFABE1',font='Futura 15')
            ]
            )
    nombreJuego = 'Juego' + str(invitado['juegos'])
    invitado['juegos'] = str(int(invitado['juegos']) + 1)
    disparos.crear(tamanio)
    for i in range(0, (tamanio) + 1):
        disparos.insertar(i,i)
    for i in range(0, (tamanio) + 1):
        #Si los botones no están vacios los limpia
        if(len(botones) > 0):
            layout.append(botones)
            botones = []
            
        for j in range(0, (tamanio)):
            boton = sg.Button(str(i) + "," + str(j), size = (4,1), font="Arial 8 bold",border_width="0")
            botones.append(boton)
    window =  sg.Window(usuario_global['nick'], layout, element_justification='c',finalize=True)
    sg.popup_ok('Es turno del jugador 2 de atacar')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            try:
                matriz.graficarNeato('1vs1')
            except:
                pass
            break
        else:
            for k in range(1 , len(layout)):
                for l in range(len(layout) - 1):
                    if(layout[k][l].ButtonText == event ):
                        if(pintar_disparo(k, l, matriz, layout)):
                            #agregar_movimiento(k-1,l,nombreJuego,usuario_global['id'])
                            invitado['monedas'] = int(invitado['monedas']) + 20
                            layout[0][1].update(invitado['monedas'])
                            #actualizar_monedas(+20)
                            puntos = puntos + 20
                        else:
                            #agregar_movimiento(k-1,l,nombreJuego,usuario_global['id'])
                            invitado['fallo'] = int(invitado['fallos']) + 1
                            Errores += 1
                        break
                else:
                    continue
                break

            if(revisar_tablero(matriz,layout)):
                
                sg.popup('Ganaste')
                break
            window.hide()
            sg.popup_ok('Turno de colocar barcos del jugador 2')
            crear_tablero(tamanio,matriz,window,layout)
            break


#Opciones de pintado para colocar barcos
def pintar_portaavion_1vs1(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
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
            matriz.insertar(x1-1, j, "P")
            layout[x1][j].update(button_color=('black', '#C98474'))
            j += 1
    #Izquierda
    elif(y2 == y1-3):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "P")
            layout[x1][j].update(button_color=('black', '#C98474'))
            j -= 1
    else:
        return False

def pintar_submarino_1vs1(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 2):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.insertar(j-1, y1, "S")
            layout[j][y1].update(button_color=('black', '#25316D'))
            j += 1
    #Arriba
    elif(x2 == x1 - 2):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "S")
            layout[j][y1].update(button_color=('black', '#25316D'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1-1, j, "S")
            layout[x1][j].update(button_color=('black', '#25316D'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 2):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "S")
            layout[x1][j].update(button_color=('black', '#25316D'))
            j -= 1
    else:
        return False

def pintar_destructor_1vs1(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 1):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.insertar(j-1, y1, "D")
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Arriba
    elif(x2 == x1 - 1):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "D")
            layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 1):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1-1, j, "D")
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 1):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "D")
            layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j -= 1
    else:
        return False

def pintar_buque_1vs1(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    if(x1 == x2 and y1 == y2):
        matriz.insertar(x1-1, y1, "B")
        layout[x1][y1].update(button_color=('black', '#6FEDD6'))
    

#Crear tablero
def crear_tablero(tamanio :int,matriz2 :MatrizDispersa, window2, layout2):
    """
    This function creates a window with a board of buttons, and then fills the board with ships
    
    :param tamanio: The size of the board
    :type tamanio: int
    """
    sg.theme('DarkTeal4')
    llenado = False
    Errores = 0
    puntos = 0
    #Si el ancho y alto es mayor a 10
    if(tamanio >= 10):
        layout = []
        botones = []
        #Numero de barcos
        constante = int(((tamanio - 1)/10)+1)
        Portaaviones = 1*constante
        Submarino = 2*constante
        Destructor = 3*constante
        Buque = 4*constante
        vidas = 3
        layout.append(
            [
            sg.Text('Puntos de ' + usuario_global['nick'] + ': ',text_color='#FFABE1',font='Futura 15'),sg.Text(usuario_global['monedas'],text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Colocar minas',button_color=('black','#FFABE1'),font='Futura 10'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text( usuario_global['nick'] + ' atacando',text_color='#FFABE1',font='Futura 15')
            ]
            )
        matriz = MatrizDispersa()
        matriz.nombre = '2'
        for i in range(0, (tamanio) + 1):
            #Si los botones no están vacios los limpia
            if(len(botones) > 0):
                layout.append(botones)
                botones = []
                
            for j in range(0, (tamanio)):
                boton = sg.Button(str(i) + "," + str(j), size = (4,1), font="Arial 8 bold",border_width="0")
                botones.append(boton)
        
        #Colocar barcos
        window =  sg.Window('Jugador 2', layout, element_justification='c',finalize=True)
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Salir':
                
                if(sg.popup_yes_no('¿Deseas regresar al menú?')):
                    sg.popup('Gracias por jugar')
                    sg.popup('Sumaste ' + str(puntos) + ' puntos')
                    sg.popup('Tuviste ' + str(Errores) + ' errores')
                    window.close()
                    break
                else:
                    sg.popup('El juego continuará')
                break
            elif(event == 'Colocar minas'):
                if (llenado == False):
                    i = 1
                    print(len(layout))
                    print("Portaaviones")
                    while i <= (Portaaviones):
                        x1 = random.randint(1, len(layout) - 1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+3
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 3
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 3
                            if(y2 <= len(layout[1])-1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 3
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                    i = 1
                    print("Submarino")
                    while i <= (Submarino):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+2
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 2
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 2
                            if(y2 <= len(layout[1])-1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 2
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                    i = 1
                    print("Destructor")
                    while i <= (Destructor):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+1
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 1
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 1
                            if(y2 <= len(layout[0])):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 1
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                    
                    i = 1
                    print("Buque")
                    while i <= (Buque):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        if(matriz.getNodo(x1-1, y1) == None):
                            print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                            pintar_buque(x1, y1, x2, y2, matriz, layout)
                            Buque -= 1
                    llenado = True
                
                    matriz.graficarNeato('Tablero')
                    sg.popup_ok('Barcos colocados correctamente')
                    sg.popup_ok('Es turno de atacar del jugador 1')
                    webbrowser.open('./matriz_Tablero.pdf')
            else:
                
                for k in range(1 , len(layout)):
                    for l in range(len(layout) - 1):
                        if(layout[k][l].ButtonText == event ):
                            disparos.conexion(k-1,l)
                            if(pintar_disparo(k, l, matriz, layout)):
                                usuario_global['monedas'] = int(usuario_global['monedas']) + 20
                                layout[0][1].update(usuario_global['monedas'])
                                puntos = puntos + 20
                            else:
                                usuario_global['fallos'] = int(usuario_global['fallos']) + 1
                                Errores += 1
                            break
                    else:
                        continue
                    break

                sg.popup_ok('Turno del jugador 2')
                window.hide()
                crear_tablero_con_matriz(matriz2, window2,layout2,matriz,window,layout)
                break


    else:
        sg.PopupError("El alto y ancho debe ser mayor a 10", title="Error")

def crear_tablero_con_matriz(matriz :MatrizDispersa, window :sg.Window, layout, matriz2 :MatrizDispersa, window2 :sg.Window, layout2):
    window.un_hide()
    vidas = 3
    Errores = 0
    puntos = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            try:
                matriz.graficarNeato('1vs1')
                if(window.Title == "Jugador 2"):
                    usuario_global['monedas'] -= 20
                sg.popup_ok('El juego ha terminado')
                sg.popup_ok(usuario_global['nick'] + ' ' + 'Ha ganado: ' + 
                    str(int(usuario_global['monedas']) - int(usuario_global['puntos'])) + ' monedas')
                sg.popup_ok('El jugador 2 ha ganado: ' + str(int(invitado['monedas']) - int(invitado['puntos'])) + ' monedas')
                break
            except:
                pass
            break
        else:
            for k in range(1 , len(layout)):
                for l in range(len(layout) - 1):
                    if(layout[k][l].ButtonText == event ):
                        if window.Title == "Jugador 2":
                            disparos.conexion(k-1,l)
                        if(pintar_disparo(k, l, matriz, layout)):
                            #agregar_movimiento(k-1,l,nombreJuego,usuario_global['id'])
                            if(window.Title == "Jugador 2"):
                                usuario_global['monedas'] = int(usuario_global['monedas']) + 20
                                layout[0][1].update(usuario_global['monedas'])
                                actualizar_monedas(+20)
                            else:
                                invitado['monedas'] = int(invitado['monedas']) + 20
                                layout[0][1].update(invitado['monedas'])
                        else:
                            #agregar_movimiento(k-1,l,nombreJuego,usuario_global['id'])
                            if(window.Title == "Jugador 2"):
                                usuario_global['fallos'] = int(usuario_global['fallos']) + 1
                            else:
                                invitado['fallos'] = int(invitado['fallos']) + 1

                            Errores += 1
                        break
                else:
                    continue
                break


            if(revisar_tablero(matriz,layout)):

                sg.popup('El ganador es ' + window2.Title)
                #Crear graphviz con datos de la partida
                try:
                    f = open('resultado.dot', 'w')
                    f.write('digraph G {\n')
                    f.write('rankdir=LR;\n')
                    f.write('node [shape=box];\n')
                    f.write('a [label="{} ha ganado: {} monedas \\n Y tuvo {} fallos"];\n'.format(
                        usuario_global['nick'], str(int(usuario_global['monedas']) - int(usuario_global['puntos'])),
                        str(usuario_global['fallos'])))
                    f.write('b [label="Jugador 2 ha ganado: {} monedas \\n Y tuvo {} fallos"];\n'.format(
                        str(int(invitado['monedas']) - int(invitado['puntos'])), str(invitado['fallos'])))

                    f.write('a;\n')
                    f.write('b;\n')
                    f.write('}')
                    f.close()
                    os.system('dot -Tpng resultado.dot -o resultado.png')
                except:
                    pass

                    



                window.close()
                window2.close()

                disparos.imprimir()
                disparos.imprimirGraphviz()
                disparos.imprimirLista()

                if(matriz.nombre == '1'):
                    matriz.graficarNeato('Tablero')
                else:
                    matriz2.graficarNeato('Tablero')
                image = Image.open('./matriz_Tablero.png')
                image = image.resize((480,480),Image.Resampling.LANCZOS)

                bio = io.BytesIO()
                image.save(bio, format='PNG')

                image2 = Image.open('./grafo.png')
                image2 = image2.resize((480,480),Image.Resampling.LANCZOS)

                bio2 = io.BytesIO()
                image2.save(bio2, format='PNG')

                image3 = Image.open('./lista.png')
                image3 = image3.resize((480,480),Image.Resampling.LANCZOS)

                bio3 = io.BytesIO()
                image3.save(bio3, format='PNG')

                image4 = Image.open('./resultado.png')
                image4 = image4.resize((480,480),Image.Resampling.LANCZOS)

                bio4 = io.BytesIO()
                image4.save(bio4, format='PNG')

                layout = [
                            [
                                [sg.Image(data = bio.getvalue(), key='imagen'),
                                sg.Image(data = bio2.getvalue(), key='imagen2')],
                                [sg.Image(data = bio3.getvalue(), key='imagen3'),
                                sg.Image(data = bio4.getvalue(), key='imagen4')]
                            
                            ]
                        ]

                window3 = sg.Window('Tablero', layout, element_justification='c')

                while True:
                    event, values = window3.read()
                    if event == sg.WIN_CLOSED:
                        break

                
                
            else:
                sg.popup_ok('Turno del ' + window.Title)
                window.hide()      
                crear_tablero_con_matriz(matriz2, window2, layout2,matriz,window,layout)
            break
            

#Portaaviones no pintado
def portaavionesNoPintado(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa):
    #Abajo
    if(x2 == x1+3):
        j = x1
        for i in range(x1, x2 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j += 1
    #Arriba
    elif(x2 == x1-3):
        j = x1
        for i in range(x2, x1 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j -= 1
    #Derecha
    elif(y2 == y1+3):
        j = y1
        for i in range(y1, y2 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j += 1
    #Izquierda
    elif(y2 == y1-3):
        j = y1
        for i in range(y2, y1 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j -= 1
    return True

#Submarino no pintado
def submarinoNoPintado(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa):
    #Abajo
    if(x2 == x1+2):
        j = x1
        for i in range(x1, x2 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j += 1
    #Arriba
    elif(x2 == x1-2):
        j = x1
        for i in range(x2, x1 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j -= 1
    #Derecha
    elif(y2 == y1+2):
        j = y1
        for i in range(y1, y2 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j += 1
    #Izquierda
    elif(y2 == y1-2):
        j = y1
        for i in range(y2, y1 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j -= 1
    return True

#Destructor no pintado
def destructorNoPintado(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa):
    #Abajo
    if(x2 == x1+1):
        j = x1
        for i in range(x1, x2 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j += 1
    #Arriba
    elif(x2 == x1-1):
        j = x1
        for i in range(x2, x1 + 1):
            if(matriz.getNodo(j-1, y1) != None):
                return False
            j -= 1
    #Derecha
    elif(y2 == y1+1):
        j = y1
        for i in range(y1, y2 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j += 1
    #Izquierda
    elif(y2 == y1-1):
        j = y1
        for i in range(y2, y1 + 1):
            if(matriz.getNodo(x1-1, j) != None):
                return False
            j -= 1
    return True


#Pintar portaavion
def pintar_portaavion(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1+3):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.insertar(j-1, y1, "P")
            #layout[j][y1].update(button_color=('black', '#C98474'))
            j += 1
    #Arriba
    elif(x2 == x1-3):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "P")
            #layout[j][y1].update(button_color=('black', '#C98474'))
            j -= 1
    #Derecha
    elif(y2 == y1+3):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1-1, j, "P")
            #layout[x1][j].update(button_color=('black', '#C98474'))
            j += 1
    #Izquierda
    elif(y2 == y1-3):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "P")
            #layout[x1][j].update(button_color=('black', '#C98474'))
            j -= 1
    else:
        return False
#Pintar submarino
def pintar_submarino(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 2):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.insertar(j-1, y1, "S")
            #layout[j][y1].update(button_color=('black', '#25316D'))
            j += 1
    #Arriba
    elif(x2 == x1 - 2):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "S")
            #layout[j][y1].update(button_color=('black', '#25316D'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 2):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1-1, j, "S")
            #layout[x1][j].update(button_color=('black', '#25316D'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 2):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "S")
            #layout[x1][j].update(button_color=('black', '#25316D'))
            j -= 1
    else:
        return False
#Pintar destructor
def pintar_destructor(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    #Abajo
    if(x2 == x1 + 1):
        j = x1
        for i in range(x1, x2 + 1):
            matriz.insertar(j-1, y1, "D")
            #layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Arriba
    elif(x2 == x1 - 1):
        j = x1
        for i in range(x2, x1 + 1):
            matriz.insertar(j-1, y1, "D")
            #layout[j][y1].update(button_color=('black', '#A2B5BB'))
            j -= 1
    #Derecha
    elif(y2 == y1 + 1):
        j = y1
        for i in range(y1, y2 + 1):
            matriz.insertar(x1-1, j, "D")
            #layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j += 1
    #Izquierda
    elif(y2 == y1 - 1):
        j = y1
        for i in range(y2, y1 + 1):
            matriz.insertar(x1-1, j, "D")
            #layout[x1][j].update(button_color=('black', '#A2B5BB'))
            j -= 1
    else:
        return False
#Pintar buque
def pintar_buque(x1 :int, y1 :int, x2 :int, y2 :int, matriz :MatrizDispersa, layout):
    if(x1 == x2 and y1 == y2):
        matriz.insertar(x1-1, y1, "B")
        #layout[x1][y1].update(button_color=('black', '#6FEDD6'))

#Pintar disparo
def pintar_disparo(x :int, y :int, matriz :MatrizDispersa, layout):
    if(matriz.getNodo(x-1, y) != None and matriz.getNodo(x-1, y).caracter == "B"):
        layout[x][y].update(button_color=('black', '#6FEDD6'))
        layout[x][y].update('X')
        matriz.getNodo(x-1, y).caracter = "XB"
        return True
    elif(matriz.getNodo(x-1, y) != None and matriz.getNodo(x-1, y).caracter == "D"):
        layout[x][y].update(button_color=('black', '#A2B5BB'))
        layout[x][y].update('X')
        matriz.getNodo(x-1, y).caracter = "XD"
        return True
    elif(matriz.getNodo(x-1, y) != None and matriz.getNodo(x-1, y).caracter == "S"):
        layout[x][y].update(button_color=('black', '#25316D'))
        layout[x][y].update('X')
        matriz.getNodo(x-1, y).caracter = "XS"
        return True
    elif(matriz.getNodo(x-1, y) != None and matriz.getNodo(x-1, y).caracter == "P"):
        layout[x][y].update(button_color=('black', '#C98474'))
        layout[x][y].update('X')
        matriz.getNodo(x-1, y).caracter = "XP"
        return True
    else:
        layout[x][y].update(button_color=('white', '#FF1E1E'))
        layout[x][y].update('X')
        matriz.insertar(x-1, y, "X")
        return False

#Revisar tablero
def revisar_tablero(matriz :MatrizDispersa,layout):
    print(matriz.nombre)
    for i in range(1 , len(layout)):
        for j in range(len(layout[1]) - 1):
            if(matriz.getNodo(i-1, j) != None and layout[i][j].ButtonText != 'X'):
                return False
    return True

#Limpiar botones
def limpiar_botones(layout):
    for i in range(1 , len(layout)):
        for j in range(len(layout) - 1):
            if(layout[i][j].ButtonColor[1] == '#EEF1FF'):
                layout[i][j].update(button_color=('#FFFFFF', '#6c7b95'))

#Actualizar monedas
def actualizar_monedas(monedas :int):
    try:
        res = requests.get(f'{base_url}/Monedas/' + str(monedas) + '/' + usuario_global['id'])
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
    except:
        print("Error al actualizar monedas")

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
            [sg.Button('Elegir skin',size = (20,1), font="Arial 15 bold")],
            [sg.Button('Regresar al menu',size = (20,1), font="Arial 15 bold")]
    ]
    window = sg.Window('Iniciar juego', layout, size=(300, 200), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Regresar al menu':
            window.close()
            break
        elif event == 'Crear Tablero':
            window.close()
            tablero_1vs1(int(sg.popup_get_text('Ingrese el tamaño de la tablero', title='Crear Tablero', size=(5, 1))))
            break
        elif event == 'Elegir skin':
            window.close()
            elegir_skin()
            break

#Elegir skin
def elegir_skin():
    try:
        res = requests.get(f'{base_url}ObtenerSkins/' + usuario_global['id'])
        skins = res.text
        skins = json.loads(skins)
        skins = skins['skins']
        layout = [[sg.Text('Elegir skin',size = (20,1), font="Arial 15 bold")]]
        for skin in skins:
            img = Image.open(skin['src'])    
            img = img.resize((100, 100), Image.ANTIALIAS)
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            data_png = bio.getvalue()
            layout.append([sg.Button(skin['nombre'],size = (10,10), font="Arial 15 bold",image_data=data_png)])
        layout.append([sg.Button('Regresar al menu',size = (20,20), font="Arial 15 bold")])
        window = sg.Window('Elegir skin', element_justification='center')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Regresar al menu':
                window.close()
                break
            else:
                sg.popup('Skin elegida', event)
                window.close()
                break
    except:
        sg.popup('Error al obtener skins')
        window.close()
        



#Llenar lista de articulos
def llenar_articulos(array_articulos):
    articulos = []
    for i in array_articulos[1]:
        articulos.append([i['nombre'] , (i['precio']), i['id'], i['src']])
    return articulos
    
#Agregar movimiento
def agregar_movimiento(x,y,nombre,id):
    try:
        res = requests.post(f'{base_url}AgregarMovimiento/' + str(x) + '/' + str(y) + '/' + str(nombre) + '/' + str(id))
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return data
    except:
        pass

#Eliminar movimiento
def eliminar_movimiento(x,y,nombre,id):
    try:
        res = requests.put(f'{base_url}AgregarMovimiento/' + str(x) + '/' + str(y) + '/' + str(nombre) + '/' + str(id))
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return data
    except:
        pass

#Obtener movimientos
def obtener_movimientos(x,y,nombre,id):
    try:
        print(f'{base_url}AgregarMovimiento/' + str(x) + '/' + str(y) + '/' + str(nombre) + '/' + str(id))
        res = requests.get(f'{base_url}AgregarMovimiento/' + str(x) + '/' + str(y) + '/' + str(nombre) + '/' + str(id))
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return data
    except:
        pass
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
                    layout[1][0].update('Monedas: ' + str(usuario_global['monedas']))
                    window.un_hide()

#Ver tutorial
def ver_tutorial():
    """
    The above function is the tutorial for the game.
    """
    data = obtener_tutorial()
    sg.theme('DarkTeal4')
    tamanio = data['ancho']
    llenado = False
    repetir = True
    monedasTutorial = 100
    #Si el ancho y alto es mayor a 10
    if(tamanio >= 10):
        layout = []
        botones = []
        #Numero de barcos
        constante = int(((tamanio - 1)/10)+1)
        Portaaviones = 1*constante
        Submarino = 2*constante
        Destructor = 3*constante
        Buque = 4*constante
        vidas = 3
        layout.append(
            [
            sg.Text('Vidas',text_color='#FFABE1',font='Futura 15'),sg.Text(vidas,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Text('Puntos',text_color='#FFABE1',font='Futura 15'),sg.Text(monedasTutorial,text_color='#FFABE1',font='Futura 15'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Colocar minas',button_color=('black','#FFABE1'),font='Futura 10'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Retroceder un movimiento',button_color=('black','#FFABE1'),font='Futura 10'),
            sg.Text('|',text_color='#FFABE1',font='Futura 15'),
            sg.Button('Siguiente Paso',button_color=('black','#FFABE1'),font='Futura 10')
            ]
            )
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
        sg.popup('Bienvenido al tutorial', title='Bienvenido')
        sg.popup('En este tutorial aprenderás a jugar el juego', title='Tutorial')
        sg.popup('En este juego debes de colocar las minas en el tablero', title='Tutorial')
        sg.popup('Para colocar una mina debes de dar click en el boton de colocar minas', title='Tutorial')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Salir':
                sg.popup('Gracias por jugar', title='Gracias')
                window.close()
                break
            elif(event == 'Retroceder un movimiento'):
                sg.popup_error('No se puede retroceder un movimiento durante el tutorial', title='Error')
            elif(event == 'Colocar minas'):
                if (llenado == False):
                    i = 1
                    print(len(layout))
                    print("Portaaviones")
                    while i <= (Portaaviones):
                        x1 = random.randint(1, len(layout) - 1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+3
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 3
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 3
                            if(y2 <= len(layout[1])-1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 3
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(portaavionesNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_portaavion(x1, y1, x2, y2, matriz, layout)
                                    Portaaviones -= 1
                            else:
                                continue
                    i = 1
                    print("Submarino")
                    while i <= (Submarino):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+2
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 2
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 2
                            if(y2 <= len(layout[1])-1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 2
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(submarinoNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_submarino(x1, y1, x2, y2, matriz, layout)
                                    Submarino -= 1
                            else:
                                continue
                    i = 1
                    print("Destructor")
                    while i <= (Destructor):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        caso = random.randint(0, 3)
                        if caso == 0:
                            x2 = x1+1
                            if(x2 <= len(layout)-1) :
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 1:
                            x2 = x1 - 1
                            if(x2 >= 1):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 2:
                            y2 = y1 + 1
                            if(y2 <= len(layout[0])):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                        elif caso == 3:
                            y2 = y1 - 1
                            if(y2 >= 0):
                                print(caso)
                                print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                                if(destructorNoPintado(x1, y1, x2, y2, matriz)):
                                    pintar_destructor(x1, y1, x2, y2, matriz, layout)
                                    Destructor -= 1
                            else:
                                continue
                    
                    i = 1
                    print("Buque")
                    while i <= (Buque):
                        x1 = random.randint(1, len(layout)-1)
                        y1 = random.randint(0, len(layout[1])-1)
                        x2 = x1
                        y2 = y1
                        if(matriz.getNodo(x1-1, y1) == None):
                            print("x1: " + str(x1-1) + " y1: " + str(y1) + " x2: " + str(x2-1) + " y2: " + str(y2))
                            pintar_buque(x1, y1, x2, y2, matriz, layout)
                            Buque -= 1
                    llenado = True
                
                    matriz.graficarNeato('Tutorial')
                    sg.popup_ok('Ya puedes comenzar a jugar', title='Tutorial')
                    sg.popup_ok('Presiona siguiente paso para seguir con el tutorial', title='Tutorial')
            elif(event == 'Siguiente Paso'):
                if(len(data['movimientos']) == 0):
                    sg.popup_ok('Ya no hay mas movimientos', title='Tutorial')
                    sg.popup_ok('Tu puntaje es: ' + str(monedasTutorial), title='Tutorial')
                    window.close()
                if(vidas > 0 and revisar_tablero(matriz,layout) == False):
                    print(data['movimientos'][0])
                    for k in range(1 , len(layout)):
                        for l in range(len(layout) - 1):
                            if(layout[k][l].ButtonText == (str(data['movimientos'][0]['x']) + ',' + str(data['movimientos'][0]['y'])) ):
                                ultimotxt = layout[k][l].ButtonText
                                if(pintar_disparo(k, l, matriz, layout)):
                                    monedasTutorial = int(monedasTutorial) + 20
                                    layout[0][4].update(monedasTutorial)
                                    data['movimientos'].pop(0)
                                    ultimo = layout[k][l]
                                    sg.popup_ok('Al acertar sumas 20 monedas', title='Tutorial')
                                else:
                                    vidas = vidas - 1
                                    layout[0][1].update(vidas)
                                    ultimo = layout[k][l]
                                    data['movimientos'].pop(0)
                                    sg.popup_ok('Al fallar pierdes una vida', title='Tutorial')
                                break
                        else:
                            continue
                        break
                else:
                    sg.popup('Perdiste', title='Tutorial')
                    if(repetir):
                        sg.popup_ok('Si tienes monedas suficientes puedes volver a jugar', title='Tutorial')
                        if((int(monedasTutorial) - 5) >= 0):
                            try:
                                ultimo.update(ultimotxt)
                                ultimo.update(button_color=('white','#6c7b95'))
                                movimiento = data['movimientos'][0]
                                print(movimiento)
                                for k in range(1 , len(layout)):
                                    for l in range(len(layout) - 1):
                                        if(layout[k][l].ButtonText == (str(data['movimientos'][0]['x']) + ',' + str(data['movimientos'][0]['y'])) ):
                                            ultimotxt = layout[k][l].ButtonText
                                            if(pintar_disparo(k, l, matriz, layout)):
                                                monedasTutorial = int(monedasTutorial) + 20
                                                layout[0][4].update(monedasTutorial)
                                                ultimo = layout[k][l]
                                                sg.popup_ok('Al acertar sumas 20 monedas', title='Tutorial')
                                            else:
                                                ultimo = layout[k][l]
                                                sg.popup_ok('Al fallar pierdes una vida', title='Tutorial')
                                            break
                                    else:
                                        continue
                                    break
                                data['movimientos'].pop(0)
                                monedasTutorial = str(int(monedasTutorial) - 5)
                                vidas += 1
                                layout[0][1].update(vidas)
                                sg.popup_ok('Se te descontaran 5 monedas por retroceder un movimiento', title='Tutorial')
                                layout[0][4].update(monedasTutorial)
                            except:
                                sg.popup_error('No hay movimientos que retroceder', title='Tutorial')
                        else:
                            sg.popup_error('No tienes suficientes monedas', title='Tutorial')
                    else:
                        break
                if(revisar_tablero(matriz,layout)):
                    sg.popup('Ganaste', title='Tutorial')
                    break
                    
            
#Agregar compra
def agregar_compra(product_id,cantidad):
    try:
        print(f'{base_url}Comprar/' + usuario_global['nick'] + '/' + usuario_global['password'] + '/' + str(product_id) + '/' + str(cantidad) + '/' )
        progress_bar()
        
        res = requests.get(f'{base_url}Comprar/' + usuario_global['nick'] + '/' + usuario_global['password'] + '/' + usuario_global['id'] + '/' + str(product_id) + '/' + str(cantidad) + '/' )
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        print(data)
        usuario_global['monedas'] = data['monedas']
        return data['status']
    except:
        sg.popup('No se pudo realizar la compra', title='Error')
        return 'errror'
            
#Obtener tutorial
def obtener_tutorial():
    """
    It makes a GET request to the API endpoint, converts the response to a dictionary, and returns the
    dictionary
    :return: A list of dictionaries
    """
    try:
        res = requests.get(f'{base_url}ObtenerTutorial/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        return data
    except:
        pass

#Comprar barcos
def comprar_articulo(data):
    img = Image.open(data[3])    
    img = img.resize((300, 300), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    data_png = bio.getvalue()
    layout = [[sg.Text('COMPRAR BARCO',size = (20,1), font="Arial 30 bold",justification='center')],
            [sg.Text('Monedas: ' + str(usuario_global['monedas']),size = (20,1), font="Arial 15 bold",justification='center')],
            [sg.Text('Nombre: ' + data[0], font="Arial 15 bold",justification='center')],
            [sg.Text('Precio: ' + str(data[1]), font="Arial 15 bold",justification='center')],
            [sg.Text('Id: ' + str(data[2]), font="Arial 15 bold",justification='center')],
            [sg.Image(data=data_png,background_color='#EEF1FF')],
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
                [sg.Button('Cerrar Sesion', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Editar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Eliminar Usuario', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Iniciar Juego', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Iniciar Tutorial', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Tienda', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(300, 430), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cerrar Sesion':
            window.close()
            login()
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
            window.hide()
            menu_reportes()
            window.un_hide()
        if event == 'Iniciar Tutorial':
            window.hide()
            ver_tutorial()
            window.un_hide()
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
            print(values)
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
            print(data)
            usuarios.append([nick, str(int(usuarios[-1][1]) + 1)])
            print(usuarios)
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
            res = requests.get(f'{base_url}ModificarUsuario/' + usuario_global['id'] + '/' + nick + '/' + usuario_global['password'] + '/' + usuario_global['edad'] + '/',timeout=5)
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
                [sg.Button('Reporte de ultima partida', size = (20,0), font="Arial 15 bold")],
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
        if event == 'Reporte de ultima partida':
            try:
                image = Image.open('./matriz_Tablero.png')
                image = image.resize((500,500),Image.Resampling.LANCZOS)

                bio = io.BytesIO()
                image.save(bio, format='PNG')

                image2 = Image.open('./grafo.png')
                image2 = image2.resize((500,500),Image.Resampling.LANCZOS)

                bio2 = io.BytesIO()
                image2.save(bio2, format='PNG')

                image3 = Image.open('./lista.png')
                image3 = image3.resize((500,500),Image.Resampling.LANCZOS)

                bio3 = io.BytesIO()
                image3.save(bio3, format='PNG')

                image4 = Image.open('./resultado.png')
                image4 = image4.resize((500,500),Image.Resampling.LANCZOS)

                bio4 = io.BytesIO()
                image4.save(bio4, format='PNG')

                layout = [
                            [
                                [sg.Image(data = bio.getvalue(), key='imagen'),
                                sg.Image(data = bio2.getvalue(), key='imagen2')],
                                [sg.Image(data = bio3.getvalue(), key='imagen3'),
                                sg.Image(data = bio4.getvalue(), key='imagen4')]
                            
                            ]
                        ]

                window3 = sg.Window('Tablero', layout, element_justification='c')

                while True:
                    event, values = window3.read()
                    if event == sg.WIN_CLOSED:
                        break
            except:
                sg.popup('No hay partida en curso')
    window.close()
    return event

#Menu Reportes Admin
def menu_reportes_admin():
    layout = [[sg.Text('Reportes',size = (10,0), font="Arial 30 bold", justification='center')],
                [sg.Button('Reportes de arbol', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de usuarios', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de compras', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Reportes de tutorial', size = (20,0), font="Arial 15 bold")],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
    window = sg.Window('Menu', layout, size=(300, 250), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Reportes de arbol':
            window.hide()
            mostrar_reportes('arbol')
            window.un_hide()
        if event == 'Reportes de compras':
            window.hide()
            mostrar_reportes('compras')
            window.un_hide()
        if event == 'Reportes de matriz de tutorial':
            webbrowser.open('./matriz_Tutorial.pdf')
        if event == 'Reportes de usuarios':
            window.hide()
            tabla_usuarios()
            window.un_hide()
    window.close()
    return event

#Tabla usuarios
def tabla_usuarios():
    try:
        res = requests.get(f'{base_url}ObtenerUsuarios/')
        data = res.text#convertimos la respuesta en dict
        data = json.loads(data)
        usuarios = []
        for usuario in data['usuarios']:
            usuarios.append([int(usuario['edad']),usuario['id'],usuario['nick'],usuario['monedas'],usuario['password']])
        layout = [
                [sg.Button('Ordenar de manera ascendente',size=(20,0),font="Arial 15 bold")],
                [sg.Button('Ordenar de manera descendente',size=(20,0),font="Arial 15 bold")],
                [sg.Table(values=usuarios, headings=['Edad','ID','Nick','Monedas','Password'], max_col_width=25, auto_size_columns=True, justification='left', num_rows=20, key='-TABLE-')],
                [sg.Button('Salir', size = (20,0), font="Arial 15 bold")]]
        window = sg.Window('Tabla Usuarios', layout, size=(500, 550), element_justification='c')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Salir':
                break
            if event == 'Ordenar de manera ascendente':
                window['-TABLE-'].update(values=sorted(usuarios, key=lambda x: x[0]))
            if event == 'Ordenar de manera descendente':
                window['-TABLE-'].update(values=sorted(usuarios, key=lambda x: x[0], reverse=True))
        window.close()
        return event == 'Salir'
    except:
        sg.popup('Error al obtener los datos', title='Error')



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


menuPrincipal()
#tablero_1vs1(10)


