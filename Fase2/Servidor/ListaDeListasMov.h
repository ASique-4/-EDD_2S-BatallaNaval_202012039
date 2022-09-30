#ifndef LISTADELISTAS_H
#define LISTADELISTAS_H
#include <stddef.h>
#include <string>
#include "nodoListas.h"

using namespace std;

class ListaDeListas {
public:
    nodoListaDeListas*primero;
    nodoListaDeListas*ultimo;
    int tamanio;
    
    ListaDeListas() {
        primero = NULL;
        ultimo = NULL;
        tamanio = 0;
    }
    void InsertarFinal(ListaMovimientos*lista);
    void Imprimir();
    void CrearGraphviz();
    ListaMovimientos* Buscar(string nombre);
    string getMovimientoComoJson();
};
#endif /* LISTADELISTAS_H */
    