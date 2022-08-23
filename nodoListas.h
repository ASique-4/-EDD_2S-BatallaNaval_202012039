#ifndef NODOLISTASDELISTAS_H
#define NODOLISTASDELISTAS_H
#include <stddef.h>
#include <string>
#include "ListaMovimientos.h"

using namespace std;

class nodoListaDeListas{
    public:
    ListaMovimientos*lista;
    ListaMovimientos*listasig;

    nodoListaDeListas(){
        lista = NULL;
        listasig = NULL;
    }
    private:
};
#endif
