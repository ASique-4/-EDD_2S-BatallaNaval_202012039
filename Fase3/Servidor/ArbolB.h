#ifndef ARBOLB_H
#define ARBOLB_H

#include <algorithm>
#include "ListaCircularUsuarios.cpp"
#include "NodoB.h"


class ArbolB {
public:
    int orden_arbol = 3;
    NodoB* raiz;
    int tamanio = 0;

    ArbolB() {
        raiz = NULL;
    }

    void eliminar(int id);
    void insertar(nodoUsuarios* usuario);
    bool login(string nick, string password, int id);
    pair<NodoB*, pair<bool, bool>> insertarCrearRama(NodoB* nodo, NodoB* rama);
    NodoB* dividir(NodoB* rama);
    pair<NodoB*, bool>  insertarEnRama(NodoB* primero, NodoB* nuevo);
    bool esHoja(NodoB* primero);
    int contador(NodoB* primero);
    void Grafo();
    string GrafoArbolAbb(NodoB*rama);
    string GrafoRamas(NodoB*rama);
    string GrafoConexionRamas(NodoB*rama);
    void agregarTodosLosUsuarios(ListaUsuarios usuarios);
    NodoB *buscar(int id);
    void insertarCompra(nodoUsuarios* usuario, nodoArticulos* articulo, int cantidad);
    void mostrarVentas(nodoUsuarios* usuario);
    string getDatosComoJson();
    string getSkinsComoJson(nodoUsuarios* usuario);
private:

};

#endif /* ARBOLB_H */

