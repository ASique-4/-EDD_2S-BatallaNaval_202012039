import os


class ListENodo():
    def __init__(self):
        self.index = 0
        self.siguiente = None
    
class ENodo():
    def __init__(self, index):
        self.index = index
        self.siguiente = None

class VNodo():
    def __init__(self):
        self.dato = None
        self.inicio = None

    
    def insertar(self, index):
        nuevo = ENodo(index)
        if self.inicio == None:
            self.inicio = nuevo
        else:
            aux = self.inicio
            while True:
                if aux.siguiente == None:
                    aux.siguiente = nuevo
                    break
                aux = aux.siguiente
    
    def imprimir(self):
        aux = self.inicio
        while aux != None:
            print('->' + '[' + str(aux.index) + ']',end='')
            aux = aux.siguiente


class ListaDG():
    def __init__(self):
        self.v = []

    def crear(self, tamanio):
        for i in range(tamanio):
            self.v.append(i)
            self.v[i] = VNodo()
    
    def insertar(self,dato,pos):
        if pos >= 0 and pos < len(self.v):
            self.v[pos].dato = dato
            self.v[pos].inicio = None

    
    def conexion(self,inicio,fin):
        if inicio >= 0 and inicio < len(self.v):
            self.v[inicio].insertar(fin)

    def imprimir(self):
        for i in self.v:
            print('[' + str(i.dato) + ']',end='')
            i.imprimir()
            print('')

    def imprimirGraphviz(self):
        f = open('grafo.dot','w')
        f.write('digraph G {\n')
        for i in self.v:
            f.write(str(i.dato) + ';\n')
            aux = i.inicio
            while aux != None:
                f.write(str(i.dato) + '->' + str(self.v[aux.index].dato) + ';\n')
                aux = aux.siguiente
        f.write('}')
        f.close()
        os.system('dot -Tpng grafo.dot -o grafo.png')


