#ifndef CABECERA_H
#define CABECERA_H
#include <stddef.h>
#include <string>


using namespace std;
class nodoCabecera {
public:
    string categoria;
    nodoCabecera*abajo;
    nodoCabecera*derecha;

    nodoCabecera() {
        abajo = NULL;
        derecha = NULL;
        categoria = ' ';

    }

};
#endif /* CABECERA_H */