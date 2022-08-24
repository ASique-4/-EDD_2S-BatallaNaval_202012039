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

void ListaArticulos::swap(nodoArticulos* a, nodoArticulos* b)
{
    int tmp_id = a->id;
    string tmp_categoria = a->categoria;
    int tmp_precio = a->precio;
    string tmp_nombre = a->nombre;
    string tmp_src = a->src;

    a->id = b->id;
    a->categoria = b->categoria;
    a->precio = b->precio;
    a->nombre = b->nombre;
    a->src = b->src;

    b->id = tmp_id;
    b->categoria = tmp_categoria;
    b->precio = tmp_precio;
    b->nombre = tmp_nombre;
    b->src = tmp_src;
}

void ListaArticulos::OrdenamientoAscendente(){
    nodoArticulos*aux = new nodoArticulos();
    aux = Inicio;
    nodoArticulos*aux2 = new nodoArticulos();
    aux2 = Inicio->sig;
    while (aux != NULL && aux2 != NULL) {
        while (aux2 != NULL) {
            if (aux->precio > aux2->precio)
            {
                swap(aux, aux2);
            }
            aux2 = aux2->sig;
        }
        aux = aux->sig;
        aux2 = aux->sig;
    }
}

void ListaArticulos::OrdenamientoDescendente(){
    nodoArticulos*aux = new nodoArticulos();
    aux = Inicio;
    nodoArticulos*aux2 = new nodoArticulos();
    aux2 = Inicio->sig;
    int i = 0;
    while (aux != NULL && aux2 != NULL) {
        while (aux2 != NULL) {
            if (aux->precio < aux2->precio)
            {
                swap(aux, aux2);
            }
            aux2 = aux2->sig;
        }
        aux = aux->sig;
        aux2 = aux->sig;
        i++;
    }
}


void ListaArticulos::Imprimir() {
    nodoArticulos*aux = new nodoArticulos();
    aux = Inicio;
    cout << "==================================Tienda=================================="<<endl;
    while(aux != NULL) {
        
        cout << "ID: " << aux->id << "  ";
        cout << "Categoria: " << aux->categoria << "  ";
        cout << "Precio: " << aux->precio << "  ";
        cout << "Nombre: " << aux->nombre << "  ";
        cout << "Src: " << aux->src << endl;
        
        aux = aux->sig;
        if (aux == NULL) {
            cout << "==========================================================================" << endl;
            cin.get();
        }
        
    }
    


}

