#include "ListaUsuarios.h"
#include "ListaDeListasMov.h"
#include <cstring>
#include <iostream>
#include <fstream>
using namespace std;

void ListaUsuarios::InsertarFinal(string nick, string password, int monedas, int edad) {
    nodoUsuarios*nuevo = new nodoUsuarios();
    nuevo->nick = nick;
    nuevo->password = password;
    nuevo->monedas = monedas;
    nuevo->edad = edad;
    nuevo->id = tamanio;
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

char* ListaUsuarios::stringtochar(std::string s){
    char*c = new char[s.length() + 1];
    strcpy(c, s.c_str());
    return c;
}

string ListaUsuarios::getUsuarioComoJson(string nick, string password) {
    nodoUsuarios*aux = primero;
    string datos = "";
    datos += "\"usuario\":[";
    while (aux != NULL) {
        if (aux->nick == nick && aux->password == password) {
            datos += "{";
            datos += "\"nick\":\"" + aux->nick + "\",";
            datos += "\"password\":\"" + aux->password + "\",";
            datos += "\"monedas\":\"" + to_string(aux->monedas) + "\",";
            datos += "\"edad\":\"" + to_string(aux->edad) + "\",";
            datos += "\"id\":\"" + to_string(aux->id) + "\"";
            datos += "}";
        }
        aux = aux->sig;
        if (aux == primero)
        {
            break;
        }
    }
    datos += "]";
    return datos;
}

void ListaUsuarios::Imprimir() {
    nodoUsuarios*aux = primero;
    printf("______________________________________________________________________________________________________\n");
    printf("| %-20s | %-64s | %-10s | %-5s | %-5s |\n", "Nick", "Password", "Monedas", "Edad", "ID");
    printf("______________________________________________________________________________________________________\n");
    while (aux != NULL) {
            
        printf("| %-20s | %-64s | %-10s | %-5s | %-5s |\n", 
        stringtochar(aux->nick), stringtochar(aux->password), stringtochar(to_string(aux->monedas)), 
        stringtochar(to_string(aux->edad)), stringtochar(to_string(aux->id)));
        aux = aux->sig;
        if (aux == primero)
        {
            printf("______________________________________________________________________________________________________\n");
            break;
        }
    }

}

string ListaUsuarios::getDatosComoJson() {
    nodoUsuarios*aux = primero;
    string datos = "";
    datos += "{";
    datos += "\"usuarios\":[";
    while (aux != NULL) {
        datos += "{";
        datos += "\"nick\":\"" + aux->nick + "\",";
        datos += "\"password\":\"" + aux->password + "\",";
        datos += "\"monedas\":\"" + to_string(aux->monedas) + "\",";
        datos += "\"edad\":\"" + to_string(aux->edad) + "\",";
        datos += "\"id\":\"" + to_string(aux->id) + "\"";
        datos += "},";
        aux = aux->sig;
        if (aux == primero)
        {
            break;
        }
    }
    //remover la ultima coma
    datos = datos.substr(0, datos.length() - 1);
    datos += "]";
    datos += "}";
    return datos;
}

bool ListaUsuarios::BuscarNick(string nick){
    nodoUsuarios*aux = primero;
    if (aux == NULL){
        return false;
    }
    while (aux != NULL) {

        if (aux->nick == nick) {
            return true;
        }
        aux = aux->sig;
        if (aux == primero)
        {
            break;
        }
    }
    return false;
}

nodoUsuarios* ListaUsuarios::BuscarUsuario(string nick, string password) {
    nodoUsuarios*aux = primero;
    if (aux == NULL){
        return NULL;
    }
    while (aux->sig != NULL) {

        if (aux->nick == nick && aux->password == password) {
            return aux;
        }
        aux = aux->sig;
        if (aux == primero)
        {
            break;
        }
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
    int temp_id = a->id;

	a->edad = b -> edad;
    a->nick = b -> nick;
    a->password = b -> password;
    a->monedas = b -> monedas;
    a->lista = b -> lista;
    a->id = b -> id;

	b -> edad = temp_edad;
    b -> nick = temp_nick;
    b -> password = temp_password;
    b -> monedas = temp_monedas;
    b -> lista = temp_listaMovimientos;
    b -> id = temp_id;

    
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
                << aux->monedas << "\n" << "ID: " << aux->id << "\"];" << endl;
                archivo << "\"" << aux->nick << "\"" << ":n->" << "\"" << aux->sig->nick << "\"" << ":s" << endl;
                archivo << "\"" << aux->nick  << "\"" << ":s->" << aux->sig->nick << "\"" << ":n" << endl;
                break;
            }else{
                archivo << "\"" << aux->nick << "\"" << "[label=\"" << "Nick: " << "\'" << aux->nick << "\'"<< "\n" 
                << "Password" << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\n" << "ID: " << aux->id << "\"];" << endl;
                archivo << aux->nick << "->" << aux->sig->nick;
                archivo << "[color = limegreen];" << endl;
            }

        }else if (aux == ultimo)
        {
            archivo << "\"" << aux->nick  << "\"" <<"[label=\"" << "Nick: " << "\'"<< aux->nick<< "\'" << "\n" 
                << "Password: " << aux->password << "\n" << "Edad: " << aux->edad << "\n" << "Monedas: " 
                << aux->monedas << "\n" << "ID: " << aux->id << "\"];" << endl;
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
                << aux->monedas << "\n" << "ID: " << aux->id << "\"];" << endl;
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

void ListaUsuarios::InsertarCompra(nodoUsuarios *usuario, nodoArticulos *articulo){
    usuario->compras = insert(usuario->compras, articulo);
}

void ListaUsuarios::MostrarCompras(nodoUsuarios *usuario){
    printTree(usuario->compras, 0);
}