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
        nuevo->ant = Ultimo;
        Ultimo = nuevo;
    }
}



void ColaTutorial::Imprimir() {
    nodoTutorial*aux = Ultimo;
    cout << "<===========Tablero===========>" << endl;
            cout << "Ancho: " << Inicio->x << endl;
            cout << "Alto: " << Inicio->y << endl;
    cout << "<=========Movimientos=========>" << endl;
    while (aux != Inicio) {
        
        if (aux->ant == Inicio){
             cout << "(" << aux->x << "," << aux->y << ")" ;
             //Salto de linea
        }else{
            cout << "(" << aux->x << "," << aux->y << ")==>" ;
        }
        
        aux = aux->ant;
        if (aux == Inicio)
        {
            cin.get();
            cout << endl;
            cout << endl;
            break;
        }
    }
}

void ColaTutorial::CrearGraphviz(){
    nodoTutorial*aux = Ultimo;
    ofstream archivo;
    archivo.open("tutorial.dot");
    archivo << "digraph Tutorial {" << endl;
    archivo << "graph [rankdir = LR ]" << endl;
    archivo << "node [shape = box]" << endl;
    int i = 0;

    while(aux != NULL) {
        if (aux == Inicio){
            archivo << i << " [label=\"" << "X: " << aux->x << "\n" << "Y: " << aux->y << "\"];" << endl;
            break;
        }else{
            archivo << i << " [label=\"" << "X: " << aux->x << "\n" << "Y: " << aux->y << "\"];" << endl;
            archivo << i << " -> " << i+1 << endl;
        }
        
        aux = aux->ant;
        i++;
    }

    archivo << "}" << endl;
    archivo.close();
    system("dot -Tpng tutorial.dot -o tutorial.png");
}