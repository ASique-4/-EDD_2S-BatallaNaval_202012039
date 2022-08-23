#ifndef CABECERA_H
#define CAEBECERA_H
#include "nodoCabecera.h"
#include "ListaArticulos.h"

#include <iostream>
using namespace std;

class Cabecera {
public:
    nodoCabecera*Inicio;
    nodoCabecera*Ultimo;
    ListaArticulos listaArticulos;

    Cabecera() {
        Inicio = NULL;
        Ultimo = NULL;
;
    }
    void InsertarFinal(string categoria);
    void InsertarArticulos(ListaArticulos listaArticulos);
    void Imprimir();
    void CrearGraphviz();
    bool Buscar(string categoria);
    private:
};

#endif /* CABECERA_H */