#ifndef LISTASUSUARIOS_H
#define LISTASUSUARIOS_H

#include "nodoUsuarios.h"

#include <iostream>
using namespace std;

class ListaUsuarios {
public:
    nodoUsuarios*primero;
    nodoUsuarios*ultimo;
    int tamanio;

    ListaUsuarios() {
        primero = NULL;
        ultimo = NULL;
        tamanio = 0;
    }
    void InsertarFinal(string nick, string password, int monedas, int edad);
    nodoUsuarios* BuscarUsuario(string nick, string password);
    void Imprimir();
    void EliminarUsuario(nodoUsuarios* usuario);
    void CrearGraphviz();
    void OrdenamientoAscendente();
    void OrdenamientoDescendente();
    void swap(nodoUsuarios* a, nodoUsuarios* b);
private:
};

#endif /* LISTASUSUARIOS_H */