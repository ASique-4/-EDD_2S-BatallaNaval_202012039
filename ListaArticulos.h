#ifndef LISTAARTICULOS_H
#define LISTAARTICULOS_H

#include "nodoArticulos.h"

#include <iostream>
using namespace std;

class ListaArticulos {
public:
    nodoArticulos*Inicio;
    int cantidad;

    ListaArticulos() {
        Inicio = NULL;
        cantidad = 0;
    }
    void InsertarFinal(int id, string categoria, int precio, string nombre, string src);
    void Imprimir();
    void InsertarCabecera(string categoria);
    void Ordenar();
    void swap(nodoArticulos* a, nodoArticulos* b);
    void OrdenamientoAscendente();
    void OrdenamientoDescendente();
    char* string_to_char(string s);
private:
};

#endif /* LISTAARTICULOS_H */