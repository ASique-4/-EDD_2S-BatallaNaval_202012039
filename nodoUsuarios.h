#ifndef NODOSUSUARIOS_H
#define NODOSUSUARIOS_H
#include <stddef.h>
#include <string>
#include "ListaMovimientos.h"

using namespace std;
class nodoUsuarios {
public:
    std::string nick;
    std::string password;
    int monedas;
    int edad;
    ListaMovimientos listaMovimientos;

    nodoUsuarios*ant;
    nodoUsuarios*sig;
    nodoUsuarios() {
        listaMovimientos = ListaMovimientos();
        ant = NULL;
        sig = NULL;
        nick = ' ';
        password = ' ';
        monedas = 0;
        edad = 0;
    }
private:
};
#endif /* NODOSUSUARIOS_H */