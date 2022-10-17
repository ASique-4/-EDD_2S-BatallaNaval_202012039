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
    cout << "<=========== Tablero ===========>" << endl;
            cout << "Ancho: " << Inicio->x << endl;
            cout << "Alto: " << Inicio->y << endl;
    cout << "<========= Movimientos =========>" << endl;
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
    archivo << "bgcolor=\"lavender\"" << endl;
    archivo << "node [ style=filled,shape = box, fillcolor=\"lavenderblush:lavenderblush1\"]" << endl;
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

string ColaTutorial::getTutorialComoJson(){
    nodoTutorial*aux = Ultimo;
    string json = "";
    json += "\"ancho\":";
    json += to_string(Inicio->x);
    json += ",";
    json += "\"alto\":";
    json += to_string(Inicio->y);
    json += ",";
    json += "\"movimientos\":[";
    while(aux != NULL) {
        if (aux == Inicio){
            json += "{\"x\":";
            json += to_string(aux->x);
            json += ",";
            json += "\"y\":";
            json += to_string(aux->y);
            json += "}";
            break;
        }else{
            json += "{\"x\":";
            json += to_string(aux->x);
            json += ",";
            json += "\"y\":";
            json += to_string(aux->y);
            json += "},";
        }
        
        aux = aux->ant;
    }
    json += "]";
    json += "}";
    return json;
}