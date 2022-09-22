#ifndef LISTAMOVIMIENTOS_H
#define LISTAMOVIMIENTOS_H

#include "nodoMovimientos.h"


#include <iostream>
using namespace std;

class ListaMovimientos {
public:
    nodoMovimientos*Inicio;
    nodoMovimientos*Ultimo;
    ListaMovimientos*sig;
    
    string nombre;

    ListaMovimientos() {
        Inicio = NULL;
        Ultimo = NULL;
        sig = NULL;
        nombre = " ";
    }
    void InsertarFinal(int x, int y);
    void Imprimir();
private:
};

#endif /* LISTAMOVIMIENTOS_H */