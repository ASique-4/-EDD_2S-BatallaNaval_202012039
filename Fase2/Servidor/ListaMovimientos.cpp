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

string ListaMovimientos::getMovimientoComoJson() {
    nodoMovimientos*aux = Inicio;
    string json = "";
    while (aux != NULL) {
        json += "{";
        json += "\"x\":";
        json += to_string(aux->x);
        json += ",";
        json += "\"y\":";
        json += to_string(aux->y);
        json += "},";
        aux = aux->sig;
    }
    return json;
}

void ListaMovimientos::EliminarUltimo() {
    if (Inicio != NULL) {
        if (Inicio == Ultimo) {
            Inicio = NULL;
            Ultimo = NULL;
        } else {
            Ultimo = Ultimo->ant;
            Ultimo->sig = NULL;
        }
    }
}