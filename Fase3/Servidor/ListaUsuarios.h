#ifndef LISTASUSUARIOS_H
#define LISTASUSUARIOS_H

#include "nodoUsuarios.h"
#include "ListaMovimientos.h"
#include "ListaDeListasMov.h"
#include "nodoArticulos.h"


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
        tamanio = 1;
    }
    void InsertarFinal(string nick, string password, int monedas, int edad, int id);
    nodoUsuarios* BuscarUsuario(string nick, string password);
    void Imprimir();
    string getDatosComoJson();
    string getUsuarioComoJson(string nick, string password);
    void EliminarUsuario(nodoUsuarios* usuario);
    void CrearGraphviz();
    void OrdenamientoAscendente();
    void OrdenamientoDescendente();
    void swap(nodoUsuarios* a, nodoUsuarios* b);
    void InsertarLista(ListaMovimientos*lista, nodoUsuarios* usuario);
    void MostrarMovimientos(nodoUsuarios* usuario);
    bool BuscarNick(string nick);
    char* stringtochar(string s);
    void InsertarCompra(nodoUsuarios* usuario, nodoArticulos* articulo, int Cantidad);
    void MostrarCompras(nodoUsuarios* usuario);
    void OrdenarPorId();
private:
};

#endif /* LISTASUSUARIOS_H */