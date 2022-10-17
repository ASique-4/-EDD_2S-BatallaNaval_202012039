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
                aux->derecha->InsertarFinal(auxArticulos->id, auxArticulos->categoria, auxArticulos->precio, 
                auxArticulos->nombre, auxArticulos->src);
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
    string label;
    label = "";
    archivo.open("tienda.dot");
    archivo << "digraph G {" << endl;
    archivo << "graph [rankdir = LR ]" << endl;
    archivo << "bgcolor=\"lavender\"" << endl;
    archivo << "node [ style=filled,shape = box, fillcolor=\"lavenderblush:lavenderblush1\"]" << endl;

    while (aux != NULL){
        rank += "\"" + aux->categoria + "\"";
        if (aux != Inicio){
            nodos += "-> \"" + aux->categoria + "\"";
        }
        aux = aux->abajo;
    }
    archivo << "{rank = same " << rank << "}" << endl;
    aux = Inicio;
    archivo << "\"" << aux->categoria << "\"" << nodos << "[color = indianred1];" << endl;

    while (aux != NULL)
    {
        archivo << "\"" << aux->categoria << "\"" << " [label=\"" << aux->categoria << "\"];" << endl;
        aux2 = aux->derecha->Inicio;
        label = "";
        while (aux2 != NULL)
        {
            label += "\"" + aux2->id + "\"" + " [label=\"" + aux2->nombre + "\"];" +"\n";
            if (aux2 == aux->derecha->Inicio){
                archivo << "\"" << aux->categoria << "\"" << "->" << "\"" << aux2->id << "\"";
            }else{
                archivo << "->" << "\"" << aux2->id << "\"";
            }
            aux2 = aux2->sig;
        }
        archivo << "[color = limegreen];" << endl;
        archivo << label;
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

string Cabecera::getArticulosComoJson() {
    //Regresa los articulos ordenados por categoria en formato json
    nodoCabecera*aux = Inicio;
    nodoArticulos*aux2;
    string json = "";
    while (aux != NULL) {
        json += "\""+aux->categoria+"\": [";
        aux2 = aux->derecha->Inicio;
        while (aux2 != NULL) {
            json += "{\"id\": \""+aux2->id+
            "\", \"categoria\": \""+aux2->categoria+
            "\", \"precio\": \""+to_string(aux2->precio)+
            "\", \"nombre\": \""+aux2->nombre+
            "\", \"src\": \""+aux2->src+"\"}";
            if (aux2->sig != NULL) {
                json += ",";
            }
            aux2 = aux2->sig;
        }
        json += "]";
        if (aux->abajo != NULL) {
            json += ",";
        }
        aux = aux->abajo;
    }
    return json;
}