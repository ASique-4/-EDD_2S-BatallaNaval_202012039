#include "CabeceraArticulos.h"
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
        while (auxArticulos != NULL) {
            if (aux->categoria == auxArticulos->categoria) {
                aux->derecha = auxArticulos;
            }
        }
    }
}
