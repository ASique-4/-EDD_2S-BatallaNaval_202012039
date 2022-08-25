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
        nuevo->ant = Ultimo;
        Ultimo = nuevo;
    }


}



void ListaMovimientos::Imprimir() {
    nodoMovimientos*aux = Inicio;
    int i = 1;
    cout << "====== " << nombre << " ======" << endl;
    while (aux != NULL) {
        cout << i <<  ". [" << aux->x << "]--";
        cout <<"[" << aux->y << "]";
        cout << endl;
        aux = aux->sig;
        i++;
    }

}