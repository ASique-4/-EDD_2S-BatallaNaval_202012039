#include "ListaMovimientos.h"
using namespace std;

void ListaMovimientos::InsertarFinal(int x, int y) {
   nodoMovimientos*nuevo = new nodoMovimientos();
    nuevo->x = x;
    nuevo->y = y;
    nuevo->sig = NULL;
    if (Inicio == NULL) {
        Inicio = nuevo;
        Ultimo = nuevo;
    } else {
        Ultimo->sig = nuevo;
        Ultimo = nuevo;
    }


}




void ListaMovimientos::Imprimir() {
    nodoMovimientos*aux = Inicio;
    while (aux != NULL) {
        cout <<"[" << aux->x << "]--";
        cout <<"[" << aux->y << "]";
        cout << endl;
        aux = aux->sig;
    }

}