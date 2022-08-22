#include "ListaMovimientos.h"
using namespace std;

void ListaMovimientos::InsertarFinal(int x, int y) {
    nodoMovimientos*nuevo = new nodoMovimientos();
    nuevo->x = x;
    nuevo->y = y;

    if (Inicio == NULL) {
        Inicio = nuevo;
    } else {
        nodoMovimientos*auxActual = Inicio;

        while (auxActual != NULL) {
            if (auxActual->sig == NULL) {
                auxActual->sig = nuevo;
                break;
            }
            auxActual = auxActual->sig;
        }
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