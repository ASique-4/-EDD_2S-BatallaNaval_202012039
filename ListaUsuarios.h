#ifndef LISTASUSUARIOS_H
#define LISTASUSUARIOS_H

#include "nodoUsuarios.h"
#include "ListaMovimientos.h"
#include "ListaDeListasMov.h"


#include <iostream>
using namespace std;

class ListaUsuarios {
public:
    nodoUsuarios*primero;
    nodoUsuarios*ultimo;
    ListaMovimientos lista;
    
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
    void InsertarLista(ListaMovimientos*lista, nodoUsuarios* usuario);
    void MostrarMovimientos(nodoUsuarios* usuario);
    bool BuscarNick(string nick);
private:
};

#endif /* LISTASUSUARIOS_H */