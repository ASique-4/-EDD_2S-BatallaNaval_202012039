#include "ListaDeListasMov.h"
#include "ListaMovimientos.h"
#include <iostream>
#include <fstream>
using namespace std;

void ListaDeListas::InsertarFinal(ListaMovimientos*movimientos) {

    if (primero == NULL) {
        primero = new nodoListaDeListas();
        ultimo = new nodoListaDeListas();
        primero->lista = movimientos;
        ultimo->lista = movimientos;
    }else{
        ultimo->listasig = movimientos;
        ultimo->lista = movimientos;
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

