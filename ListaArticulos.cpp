#include "ListaArticulos.h"
#include <iostream>
#include <fstream>
using namespace std;

void ListaArticulos::InsertarFinal(int id, string categoria, int precio, string nombre, string src) {
    nodoArticulos*nuevo = new nodoArticulos();
    nuevo->id = id;
    nuevo->categoria = categoria;
    nuevo->precio = precio;
    nuevo->nombre = nombre;
    nuevo->src = src;
    cantidad++;
    if (Inicio == NULL) {
        Inicio = nuevo;
    } else {
        nodoArticulos*auxActual = Inicio;

        while (auxActual != NULL) {
            if (auxActual->sig == NULL) {
                auxActual->sig = nuevo;
                break;
            }
            auxActual = auxActual->sig;
        }
    }


}


void ListaArticulos::Imprimir() {
    nodoArticulos*aux = Inicio;
    cout << "==================================Tienda=================================="<<endl;
    while(aux != NULL) {
        
        cout << "ID: " << aux->id << "  ";
        cout << "Categoria: " << aux->categoria << "  ";
        cout << "Precio: " << aux->precio << "  ";
        cout << "Nombre: " << aux->nombre << "  ";
        cout << "Src: " << aux->src << endl;
        
        aux = aux->sig;
    }
    cout << "==========================================================================" << endl;

}

void ListaArticulos::CrearGraphviz(){
    nodoArticulos*aux = Inicio;
    ofstream archivo;
    archivo.open("tienda.dot");
    archivo << "digraph Tienda {" << endl;
    while(aux != NULL) {
        archivo << aux->id << " [label=\"" << aux->nombre << "\"];" << endl;
        aux = aux->sig;
    }
    aux = Inicio;
    while(aux != NULL) {
        if(aux->sig != NULL) {
            archivo << aux->id << " -> " << aux->sig->id << ";" << endl;
        }
        aux = aux->sig;
    }
    archivo << "}" << endl;
    archivo.close();
    system("dot -Tpng tienda.dot -o tienda.png");
}