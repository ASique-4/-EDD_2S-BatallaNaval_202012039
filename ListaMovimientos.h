#ifndef LISTAMOVIMIENTOS_H
#define LISTAMOVIMIENTOS_H

#include "nodoMovimientos.h"

#include <iostream>
using namespace std;

class ListaMovimientos {
public:
    nodoMovimientos*Inicio;

    ListaMovimientos() {
        Inicio = NULL;
    }
    void InsertarFinal(int x, int y);
    void Imprimir();
private:
};

#endif /* LISTAMOVIMIENTOS_H */