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
    int i = 0;
    cout << aux->lista->nombre << endl;
    while(aux != NULL) {
        cout << i << " -> " << aux->lista->nombre << endl;
        aux2 = aux->lista->Inicio;
        while (aux2 != NULL) {
            
            if (aux2 == aux->lista->Ultimo){
                archivo << i << " [label=\"" << "X: " << aux2->x << "\n" << "Y: " << aux2->y << "\"];" << endl;
                break;
            }else{
                archivo << i << " [label=\"" << "X: " << aux2->x << "\n" << "Y: " << aux2->y << "\"];" << endl;
                archivo << i << " -> " << i+1 << endl;
            }
            aux2 = aux2->sig;
        }
        aux = aux->sigNodo;
        i++;
    }
    archivo << "}" << endl;
    archivo.close();
    system("dot -Tpng pila.dot -o pila.png");
}

