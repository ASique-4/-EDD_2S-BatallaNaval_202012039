#include "ListaDeListasMov.h"
#include "ListaMovimientos.h"
#include <iostream>
#include <fstream>
using namespace std;

void ListaDeListas::InsertarFinal(ListaMovimientos*movimientos) {
    nodoListaDeListas*aux;
    aux = new nodoListaDeListas();
    aux->lista = movimientos;
    aux->sigNodo = NULL;
    if (primero == NULL) {
        primero = new nodoListaDeListas();
        ultimo = new nodoListaDeListas();
        primero = aux;
        ultimo = aux;
    }else{
        
        ultimo->sigNodo = aux;
        ultimo = aux;
    }
}

void ListaDeListas::Imprimir(){
    nodoListaDeListas*aux;
    aux = new nodoListaDeListas();
    aux->lista = primero->lista;
    while (aux->lista != NULL) {
        aux->lista->Imprimir(); 
        aux->lista = aux->listasig;
    }
}

void ListaDeListas::CrearGraphviz(){
    nodoListaDeListas*aux;
    nodoMovimientos*aux2;
    aux2 = new nodoMovimientos();
    aux = new nodoListaDeListas();
    aux = primero;
    ofstream archivo;
    archivo.open("pila.dot");
    archivo << "digraph Tutorial {" << endl;
    archivo << "graph [rankdir = LR ]" << endl;
    archivo << "node [shape = box]" << endl;
    archivo << "bgcolor=\"lavender\"" << endl;
    archivo << "node [ style=filled,shape = box, fillcolor=\"lavenderblush:lavenderblush1\"]" << endl;
    int i = 0;
    cout << "\"" <<  aux->lista->nombre << "\"" << endl;
    string rank;
    string nodos;
    string felchas;
    felchas = "";
    while (aux != NULL){
        rank += "\"" + aux->lista->nombre + "\"";
        if (aux != primero){
            nodos += "-> \"" + aux->lista->nombre + "\"";
        }
        aux = aux->sigNodo;
    }
    archivo << "{rank = same " << rank << "}" << endl;
    aux = primero;
    archivo << "\"" << aux->lista->nombre << "\"" << nodos << "[color = indianred1];" << endl;
    
    while(aux != NULL) {
        archivo << "\"" << aux->lista->nombre << "\"" << " [label=\"" << aux->lista->nombre << "\"];" << endl;
        aux2 = aux->lista->Ultimo;
        while (aux2 != NULL) {
            archivo << i<< " [label=\"" << "X: " << aux2->x << "\n" << "Y: " << aux2->y << "\"];" << endl;
            if (aux2 == aux->lista->Ultimo){
                felchas +=   "\"" + aux->lista->nombre + "\"" + "->" + to_string(i);
            }else{
                felchas += " -> " +to_string(i);
            }
            aux2 = aux2->ant;
            
            i++;
        }
        aux = aux->sigNodo;
        archivo << felchas << "[color = limegreen]; " << endl;
        felchas = "";
        archivo << endl;
        
    }
    archivo << "}" << endl;
    archivo.close();
    system("dot -Tpng pila.dot -o pila.png");
}

