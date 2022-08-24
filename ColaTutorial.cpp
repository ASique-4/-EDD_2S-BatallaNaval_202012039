#include "ListaTutorial.h"
#include "ListaMovimientos.h"
#include <iostream>
#include <fstream>
using namespace std;

void ColaTutorial::InsertarFinal(int x, int y) {
    nodoTutorial*nuevo = new nodoTutorial();
    nuevo->x = x;
    nuevo->y = y;
    if (Inicio == NULL) {
        Inicio = nuevo;
        Ultimo = nuevo;
    } else {
        Ultimo->sig = nuevo;
        Ultimo = nuevo;
    }
}



void ColaTutorial::Imprimir() {
    nodoTutorial*aux = Inicio;
    while (aux != NULL) {
        if (aux == Inicio)
        {
            cout << "<===========Tablero===========>" << endl;
            cout << "Ancho: " << aux->x << endl;
            cout << "Alto: " << aux->y << endl;
            cout << "<=========Movimientos=========>" << endl;
        }else if (aux == Ultimo){
             cout << "(" << aux->x << "," << aux->y << ")" << endl;
             //Salto de linea
                cout << endl;
                cout << endl;
        }else{
            cout << "(" << aux->x << "," << aux->y << ")=>" ;
        }
        
        aux = aux->sig;
    }
}

void ColaTutorial::CrearGraphviz(){
    nodoTutorial*aux = Inicio;
    ofstream archivo;
    archivo.open("tutorial.dot");
    archivo << "digraph Tutorial {" << endl;
    archivo << "graph [rankdir = LR ]" << endl;
    archivo << "node [shape = box]" << endl;
    int i = 0;

    while(aux != NULL) {
        if (aux == Ultimo){
            archivo << i << " [label=\"" << "X: " << aux->x << "\n" << "Y: " << aux->y << "\"];" << endl;
            break;
        }else{
            archivo << i << " [label=\"" << "X: " << aux->x << "\n" << "Y: " << aux->y << "\"];" << endl;
            archivo << i << " -> " << i+1 << endl;
        }
        
        aux = aux->sig;
        i++;
    }

    archivo << "}" << endl;
    archivo.close();
    system("dot -Tpng tutorial.dot -o tutorial.png");
}