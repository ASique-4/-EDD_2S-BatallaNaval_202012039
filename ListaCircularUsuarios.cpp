#include "ListaUsuarios.h"
#include "ListaDeListasMov.h"
#include <iostream>
#include <fstream>
using namespace std;

void ListaUsuarios::InsertarFinal(string nick, string password, int monedas, int edad) {
    nodoUsuarios*nuevo = new nodoUsuarios();
    nuevo->nick = nick;
    nuevo->password = password;
    nuevo->monedas = monedas;
    nuevo->edad = edad;
    tamanio++;
    if (primero == NULL) {
        primero = nuevo;
        ultimo = nuevo;
        primero -> sig=primero;
        primero -> ant=ultimo;
    } else {
        ultimo->sig = nuevo;
        nuevo->ant = ultimo;
        ultimo = nuevo;
        ultimo -> sig=primero;
        primero -> ant=ultimo;
    }
}

void ListaUsuarios::InsertarLista(ListaMovimientos*movimientos, nodoUsuarios*usuario){
    usuario->lista.InsertarFinal(movimientos);
}

void ListaUsuarios::Imprimir() {
    nodoUsuarios*aux = primero;
    while (aux != NULL) {
        cout << "====================" << endl;
        cout << "Nick: " << aux->nick << endl;
        cout << "Password: " << aux->password << endl;
        cout << "Monedas: " << aux->monedas << endl;
        cout << "Edad: " << aux->edad << endl;
        cout << "====================" << endl;
        aux = aux->sig;
        if (aux == primero)
        {
            cin.get();
            break;
        }
    }

}

bool ListaUsuarios::BuscarNick(string nick){
    nodoUsuarios*aux = primero;
    if (aux == NULL){
        return false;
    }
    while (aux->sig != primero) {

        if (aux->nick == nick) {
            return true;
        }
        aux = aux->sig;
    }
    return false;
}

nodoUsuarios* ListaUsuarios::BuscarUsuario(string nick, string password) {
    nodoUsuarios*aux = primero;
    if (aux == NULL){
        return NULL;
    }
    while (aux->sig != primero) {

        if (aux->nick == nick && aux->password == password) {
            return aux;
        }
        aux = aux->sig;
    }
    return NULL;
}

void ListaUsuarios::EliminarUsuario(nodoUsuarios* aux)
{
    if (aux == primero)
    {
        if (primero == ultimo)
        {
            primero = NULL;
            ultimo = NULL;
        }
        else
        {
            primero = primero->sig;
            primero->ant = ultimo;
            ultimo->sig = primero;
        }
    }
    else if (aux == ultimo)
    {
        ultimo = ultimo->ant;
        ultimo->sig = primero;
        primero->ant = ultimo;
    }
    else
    {
        aux->ant->sig = aux->sig;
        aux->sig->ant = aux->ant;
    }
    delete aux;
}

void ListaUsuarios::swap(nodoUsuarios* a, nodoUsuarios* b)
{
    int temp_edad = a->edad;
    string temp_nick = a->nick;
    string temp_password = a->password;
    int temp_monedas = a->monedas;
    ListaDeListas temp_listaMovimientos = a->lista;

	a->edad = b -> edad;
    a->nick = b -> nick;
    a->password = b -> password;
    a->monedas = b -> monedas;
    a->lista = b -> lista;

	b -> edad = temp_edad;
    b -> nick = temp_nick;
    b -> password = temp_password;
    b -> monedas = temp_monedas;
    b -> lista = temp_listaMovimientos;

    
}

void ListaUsuarios::OrdenamientoAscendente(){
    nodoUsuarios*aux = primero;
    nodoUsuarios*aux2 = primero->sig;
    while (aux != ultimo) {
        while (aux2 != primero) {
            if (aux->edad > aux2->edad)
            {
                swap(aux, aux2);
            }
            aux2 = aux2->sig;
        }
        aux = aux->sig;
        aux2 = aux->sig;
    }
}

void ListaUsuarios::OrdenamientoDescendente(){
    nodoUsuarios*aux = primero;
    nodoUsuarios*aux2 = primero->sig;
    while (aux != ultimo) {
        while (aux2 != primero) {
            if (aux->edad < aux2->edad)
            {
                swap(aux, aux2);
            }
            aux2 = aux2->sig;
        }
        aux = aux->sig;
        aux2 = aux->sig;
    }
}

void ListaUsuarios::CrearGraphviz()
{
    nodoUsuarios*aux = primero;
    ofstream archivo;
    archivo.open("usuarios.dot");
    archivo << "digraph G {" << endl;
    archivo << "graph [rankdir = TB ]" << endl;
    archivo << "node [shape = box]" << endl;
    archivo << "bgcolor=\"lavender\"" << endl;
    archivo << "node [ style=filled,shape = box, fillcolor=\"lavenderblush:lavenderblush1\"]" << endl;

    while (aux != NULL)
    {
        if (aux == primero)
        {
            if (aux->sig==primero)
            {
                
                archivo << "\"" << aux->nick  << "\"" << " [label=\"" << "Nick: " << "\'" << aux->nick << "\'" << "\n" 
                << "Password" << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\"];" << endl;
                archivo << "\"" << aux->nick << "\"" << ":n->" << "\"" << aux->sig->nick << "\"" << ":s" << endl;
                archivo << "\"" << aux->nick  << "\"" << ":s->" << aux->sig->nick << "\"" << ":n" << endl;
                break;
            }else{
                archivo << "\"" << aux->nick << "\"" << "[label=\"" << "Nick: " << "\'" << aux->nick << "\'"<< "\n" 
                << "Password" << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\"];" << endl;
                archivo << aux->nick << "->" << aux->sig->nick;
                archivo << "[color = limegreen];" << endl;
            }

        }else if (aux == ultimo)
        {
            archivo << "\"" << aux->nick  << "\"" <<"[label=\"" << "Nick: " << "\'"<< aux->nick<< "\'" << "\n" 
                << "Password: " << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\"];" << endl;
            archivo << "\"" << aux->nick << "\"" << "->" << "\"" << aux->ant->nick << "\"" ;
            archivo << "[color = indianred1];" << endl;
            archivo << "\"" << aux->nick << "\"" << ":e->" << "\"" << aux->sig->nick << "\"" << ":e";
            archivo << "[color = limegreen];" << endl;
            archivo << "\"" << aux->sig->nick << "\"" << ":w->" << "\"" << aux->nick << "\"" << ":w";
            archivo << "[color = indianred1];" << endl;
            break;
        }else{
            archivo << "\"" << aux->nick << "\"" << " [label=\"" << "Nick: " << "\'" << aux->nick << "\'" << "\n" 
                << "Password" << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\"];" << endl;
            archivo << "\"" << aux->nick << "\"" << "->" << "\"" << aux->sig->nick << "\"" ;
            archivo << "[color = limegreen];" << endl;
            archivo << "\"" << aux->nick << "\"" << "->" << "\"" << aux->ant->nick << "\"" ;
            archivo << "[color = indianred1];" << endl;
        }
        aux = aux->sig;
        
    }

    archivo << "}";
    archivo.close();
    system("dot -Tpng usuarios.dot -o usuarios.png");
}

void ListaUsuarios::MostrarMovimientos(nodoUsuarios *usuario){
    nodoListaDeListas*movimientos = new nodoListaDeListas();
    movimientos = usuario->lista.primero;
    while(movimientos != NULL){
        cout << movimientos->lista->nombre << endl;
        movimientos->lista->Imprimir();
        if (movimientos == usuario->lista.ultimo){
            break;
        }
        movimientos = movimientos->sigNodo;
    }
}
