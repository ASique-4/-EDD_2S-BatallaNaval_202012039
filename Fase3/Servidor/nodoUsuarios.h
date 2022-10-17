#ifndef NODOSUSUARIOS_H
#define NODOSUSUARIOS_H
#include <stddef.h>
#include <string>
#include "ListaMovimientos.h"
#include "ListaDeListasMov.h"
#include "ComprasAVL.cpp"

using namespace std;
class nodoUsuarios {
public:
    std::string nick;
    std::string password;
    int monedas;
    int edad;
    ListaDeListas lista;
    int id;
    node *compras;


    nodoUsuarios*ant;
    nodoUsuarios*sig;
    nodoUsuarios() {
   
        ant = NULL;
        sig = NULL;
        nick = ' ';
        password = ' ';
        monedas = 0;
        edad = 0;
        id = 0;
        compras = NULL;
    }
private:
};
#endif /* NODOSUSUARIOS_H */