#include "CabeceraArticulos.h"
#include "ListaArticulos.h"
#include <iostream>
#include <fstream>
using namespace std;

void Cabecera::InsertarFinal(string categoria) {
    nodoCabecera*nuevo = new nodoCabecera();
    nuevo->categoria = categoria;
    nuevo->abajo = NULL;
    if (Inicio == NULL) {
        Inicio = nuevo;
        Ultimo = nuevo;
    } else {
        Ultimo->abajo = nuevo;
        Ultimo = nuevo;
    }
}

void Cabecera::InsertarArticulos(ListaArticulos listaArticulos) {
    nodoCabecera*aux = Inicio;
    nodoArticulos*auxArticulos = listaArticulos.Inicio;
    while (aux != NULL) {
        auxArticulos = listaArticulos.Inicio;
        while (auxArticulos != NULL) {
            if (aux->categoria == auxArticulos->categoria) {
                aux->derecha->InsertarFinal(auxArticulos->id, auxArticulos->categoria, auxArticulos->precio, auxArticulos->nombre, auxArticulos->src);
            }
            auxArticulos = auxArticulos->sig;
        }
        aux = aux->abajo;
    }
}

void Cabecera::Imprimir() {
    nodoCabecera*aux = Inicio;
    while (aux != NULL) {
        cout << "Categoria: " << aux->categoria << endl;
        aux->derecha->Imprimir();
        aux = aux->abajo;
    }
}

void Cabecera::CrearGraphviz() {
    nodoCabecera*aux = Inicio;
    nodoArticulos*aux2;
    ofstream archivo;
    string rank;
    string nodos;
    archivo.open("tienda.dot");
    archivo << "digraph G {" << endl;
    archivo << "graph [rankdir = LR ]" << endl;
    archivo << "node [shape = box]" << endl;

    while (aux != NULL){
        rank += "\"" + aux->categoria + "\"";
        if (aux != Inicio){
            nodos += "-> \"" + aux->categoria + "\"";
        }
        aux = aux->abajo;
    }
    archivo << "{rank = same " << rank << "}" << endl;
    aux = Inicio;
    archivo << aux->categoria << nodos << endl;

    while (aux != NULL)
    {
        archivo << aux->categoria << " [label=\"" << aux->categoria << "\"];" << endl;
        aux2 = aux->derecha->Inicio;
        while (aux2 != NULL)
        {
            if (aux2 == aux->derecha->Inicio){
                archivo << "\"" << aux->categoria << "\"" << "->" << aux2->nombre;
            }else{
                archivo << "->" << "\"" << aux2->nombre << "\"";
            }

            
            aux2 = aux2->sig;
        }
        archivo << endl;

        aux = aux->abajo;
        
    }

    archivo << "}";
    archivo.close();
    system("dot -Tpng tienda.dot -o tienda.png");
}

bool Cabecera::Buscar(string categoria) {
    nodoCabecera*aux = Inicio;
    while (aux != NULL) {
        if (aux->categoria == categoria) {
            return true;
            break;
        }
        aux = aux->abajo;
    }
    return false;
}
