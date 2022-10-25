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
        """
        It creates a new node, and if the list is empty, it makes the new node the first node in the
        list. Otherwise, it finds the last node in the list and makes the new node the last node in the
        list
        
        :param index: The index of the node to be inserted
        """
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
        """
        It inserts a node at a given position in a linked list
        
        :param dato: the data to be inserted
        :param pos: position of the element to be inserted
        """
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
        f.write('bgcolor="#5DA7DB"\n')
        f.write('node [ style=filled,shape = oval, fillcolor="lightblue:lightblue1"]\n')
        for i in self.v:
            aux = i.inicio
            while aux != None:
                f.write(str(i.dato) + '->' + str(self.v[aux.index].dato) + ';\n')
                aux = aux.siguiente
        f.write('}')
        f.close()
        os.system('dot -Tpng grafo.dot -o grafo.png')
    
    def imprimirLista(self):
        f = open('lista.dot','w')
        f.write('digraph G {\n')
        f.write('graph [rankdir = LR ]\n')
        f.write('nodesep = 0\n')
        f.write('bgcolor="#5DA7DB"\n')
        f.write('node [ style=filled,shape = box, fillcolor="lavenderblush:lavenderblush1"]\n')
        rank = '{rank = same; '
        label = ''
        apuntador = ''
        for i in self.v:
            rank += "\"" + "i" + str(i.dato) + "i\" "
            label += "\"" + "i" + str(i.dato) + "i\" " + "[label = \"" + str(i.dato) + "\"]\n"
            apuntador += "\"" + "i" + str(i.dato) + "i\" " + "->"
        f.write(rank + '};\n')
        f.write(label + '\n')
        apuntador = apuntador[:-2]
        f.write(apuntador + ' [arrowhead = none]\n')
        for i in self.v:
            aux = i.inicio
            apuntador = ''
            count = 0
            while aux != None:
                f.write('i' + str(i.dato) + 'i' + str(self.v[aux.index].dato) + ' [label = \"' + str(self.v[aux.index].dato) + '\", fillcolor="lightblue:lightblue1"];\n')
                apuntador += 'i' + str(i.dato) + 'i' + str(self.v[aux.index].dato) + '->'
                aux = aux.siguiente
                count += 1
            
            if count > 0:
                apuntador = apuntador[:-2]
                f.write( 'i' + str(i.dato) + 'i->' + apuntador + '\n')
           
            
        f.write('}')
        f.close()
        os.system('dot -Tpng lista.dot -o lista.png')




lista = ListaDG()
lista.crear(12)

lista.insertar(0,0)
lista.insertar(1,1)
lista.insertar(2,2)
lista.insertar(3,3)
lista.insertar(4,4)
lista.insertar(5,5)
lista.insertar(6,6)
lista.insertar(7,7)
lista.insertar(8,8)
lista.insertar(9,9)
lista.insertar(10,10)
lista.insertar(11,11)

lista.conexion(0,2)
lista.conexion(0,3)
lista.conexion(0,4)
lista.conexion(1,1)
lista.conexion(1,2)
lista.conexion(1,5)
lista.conexion(2,1)
lista.conexion(2,2)
lista.conexion(2,8)
lista.conexion(3,1)
lista.conexion(5,3)
lista.conexion(5,5)
lista.conexion(5,7)
lista.conexion(5,8)
lista.conexion(5,10)
lista.conexion(5,11)
lista.conexion(6,1)
lista.conexion(6,7)
lista.conexion(6,8)
lista.conexion(6,10)
lista.conexion(7,1)
lista.conexion(7,7)
lista.conexion(7,8)
lista.conexion(7,10)
lista.conexion(8,1)
lista.conexion(8,5)
lista.conexion(8,10)
lista.conexion(9,1)
lista.conexion(9,4)
lista.conexion(9,9)
lista.conexion(9,10)
lista.conexion(9,11)
lista.conexion(10,1)
lista.conexion(10,7)
lista.conexion(10,9)
lista.conexion(10,10)
lista.conexion(11,7)


lista.imprimir()
lista.imprimirGraphviz()
lista.imprimirLista()