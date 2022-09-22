#ifndef CABECERA_H
#define CABECERA_H
#include <stddef.h>
#include <string>


using namespace std;
class nodoCabecera {
public:
    string categoria;
    nodoCabecera*abajo;
    ListaArticulos*derecha;

    nodoCabecera() {
        abajo = NULL;
        derecha = new ListaArticulos();
        categoria = ' ';

    }

};
#endif /* CABECERA_H */