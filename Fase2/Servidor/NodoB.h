#ifndef NODOB_H
#define NODOB_H

#include <stddef.h>
#include <iostream>
using namespace std;

class NodoB {
public:
    nodoUsuarios*usuario;
    //Apuntadores dentro de la rama
    NodoB* siguiente;
    NodoB* anterior;

    //apuntadores al inicio de otra rama
    NodoB* derecha;
    NodoB* izquierda;

    NodoB(nodoUsuarios*user) {
        usuario = user;
        siguiente = NULL;
        anterior = NULL;
        derecha = NULL;
        izquierda = NULL;
    }
private:

};

#endif /* NODOB_H */

