#include "ArbolB.h"

#include <fstream>
#include <string>
#include <sstream>
#include <iostream>


void ArbolB::insertar(nodoUsuarios* usuario) {
    tamanio++;
    NodoB* nodo = new NodoB(usuario);
    if (raiz == NULL) {
        raiz = nodo;
    } else {
        pair < NodoB*, pair<bool, bool>> ret = insertarCrearRama(nodo, raiz);
        NodoB* obj = ret.first;
        if ((ret.second.first or ret.second.second) and obj != NULL) {//si se divide la rama o se inserta al inicio, la raiz cambia
            cout << "se cambia de rama principal ID:" << obj->usuario->id << "\n";
            raiz = obj;
        }
    }
}

/**
 * Metodo recorre el arbol e inserta los valores nuevos, verifica si es necesario dividir ramas
 *
 * @param NodoB* nodo es el nodo a insertar
 * @param NodoB* rama es la rama en la cual se inicia la busqueda de la posicion donde insertarlo
 * 
 * @retun retorna un listado de elementos que nos permiten identificar lo siguiente:
 * 
 * NodoB*: nodo inicial de la rama donde se inserto un elemento
 * 
 * bool: true or false indicando si una rama se dividio en dos nuevas
 * 
 * bool: true or false indicando si el inicio de la rama cambio debio a un insert al inicio.
 */
pair<NodoB*, pair<bool, bool>> ArbolB::insertarCrearRama(NodoB* nodo, NodoB* rama) {
    pair < NodoB*, pair<bool, bool>> ResultadoRama;
    ResultadoRama.first = NULL; //nodo Inicial de la rama
    ResultadoRama.second.first = false; //indica si se dividio la rama
    ResultadoRama.second.second = false; //indica si se modifica el inicio de la rama
    if (esHoja(rama)) {//si el nodo es hoja se inseta directamente dentro de ella
        pair < NodoB*, bool> resultado = insertarEnRama(rama, nodo); //insertamos el nuevo elemento dentro de la rama actual
        ResultadoRama.first = resultado.first; //posee la rama con el valor ya insertado
        ResultadoRama.second.second = resultado.second; //posee el resultado de si se modifico el inicio en el insert anterior
        if (contador(resultado.first) == orden_arbol) {//si la rama posee mas elementos de los permitidos se divide
            cout << "La rama debe dividirse\n";
            cout << "ID:" << resultado.first->usuario->id << "\n";
            ResultadoRama.first = dividir(resultado.first); //dividimos la rama y obtenemos una nueva rama con sus respectivos apuntadores
            ResultadoRama.second.first = true; //identificar que la rama se dividio
        }
    } else {//si el nodo es rama se debe buscar la posicion donde insertarlo
        NodoB*temp = rama;
        do {
            if (nodo->usuario->id == temp->usuario->id) {//valor ya insertado, no se permiten repeditos
                cout << "insertarCrearRama(), El ID " << nodo->usuario->id << " ya existe\n";
                return ResultadoRama;
            } else if (nodo->usuario->id < temp->usuario->id) {
                pair < NodoB*, pair<bool, bool>> ResultadoInsert = insertarCrearRama(nodo, temp->izquierda);
                if (ResultadoInsert.second.second and ResultadoInsert.first != NULL) {//si se modifico el inicio de la rama
                    ResultadoRama.second.second = true;
                    temp->izquierda = ResultadoInsert.first;
                }
                if (ResultadoInsert.second.first) {//se dividio la subrama
                    pair < NodoB*, bool> auxInsert = insertarEnRama(rama, ResultadoInsert.first);
                    rama = auxInsert.first;
                    if (auxInsert.second) {
                        ResultadoRama.first = rama;
                    }
                    if (contador(rama) == orden_arbol) {
                        ResultadoRama.first = dividir(rama);
                        ResultadoRama.second.first = true;
                    }
                }
                return ResultadoRama;
            } else if (temp->siguiente == NULL) {
                pair < NodoB*, pair<bool, bool>> ResultadoInsert = insertarCrearRama(nodo, temp->derecha);
                if (ResultadoInsert.second.second and ResultadoInsert.first != NULL) {//si se modifico el inicio de la rama
                    ResultadoRama.second.second = true;
                    temp->derecha = ResultadoInsert.first;
                }
                if (ResultadoInsert.second.first) {//se dividio la subrama
                    pair < NodoB*, bool> auxInsert = insertarEnRama(rama, ResultadoInsert.first);
                    rama = auxInsert.first;
                    if (auxInsert.second) {
                        ResultadoRama.first = rama;
                    }
                    if (contador(rama) == orden_arbol) {
                        ResultadoRama.first = dividir(rama);
                        ResultadoRama.second.first = true;
                    }
                }
                return ResultadoRama;
            }
            temp = temp->siguiente;
        } while (temp != NULL);
    }
    return ResultadoRama;
}

NodoB* ArbolB::dividir(NodoB* rama) {
    int val = -999;
    NodoB*temp = NULL;
    NodoB*Nuevito = NULL;
    NodoB*aux = rama;

    NodoB*rderecha = NULL;
    NodoB*rizquierda = NULL;

    int cont = 0;
    while (aux != NULL) {
        cont++;
        //implementacion para dividir unicamente ramas de 4 nodos
        if (cont < 3) {
            val = aux->usuario->id;
            temp = new NodoB(aux->usuario);
            temp->izquierda = aux->izquierda;
            if (cont == 2) {
                temp->derecha = aux->siguiente->izquierda;
            } else {
                temp->derecha = aux->derecha;
            }
            rizquierda = insertarEnRama(rizquierda, temp).first;
        } else if (cont == 3) {
            val = aux->usuario->id;
            Nuevito = new NodoB(aux->usuario);
        } else {
            val = aux->usuario->id;
            temp = new NodoB(aux->usuario);
            temp->izquierda = aux->izquierda;
            temp->derecha = aux->derecha;
            rderecha = insertarEnRama(rderecha, temp).first;
        }
        aux = aux->siguiente;
    }
    Nuevito->derecha = rderecha;
    Nuevito->izquierda = rizquierda;
    return Nuevito;
}

pair<NodoB*, bool> ArbolB::insertarEnRama(NodoB* primero, NodoB* nuevo) {
    pair < NodoB*, bool> ret;
    ret.second = false;
    if (primero == NULL) {
        //primero en la lista
        ret.second = true;
        primero = nuevo;
    } else {
        //recorrer e insertar
        NodoB* aux = primero;
        while (aux != NULL) {
            if (aux->usuario->id == nuevo->usuario->id) {//------------->ya existe en el arbol
                cout << "insertarEnRama(), El ID " << nuevo->usuario->id << " ya existe\n";
                break;
            } else {
                if (aux->usuario->id > nuevo->usuario->id) {
                    if (aux == primero) {//------------->insertar al inicio
                        aux->anterior = nuevo;
                        nuevo->siguiente = aux;
                        //ramas del nodo
                        aux->izquierda = nuevo->derecha;
                        nuevo->derecha = NULL;
                        ret.second = true;
                        primero = nuevo;
                        break;
                    } else {//------------->insertar en medio;
                        nuevo->siguiente = aux;
                        //ramas del nodo
                        aux->izquierda = nuevo->derecha;
                        nuevo->derecha = NULL;

                        nuevo->anterior = aux->anterior;
                        aux->anterior->siguiente = nuevo;
                        aux->anterior = nuevo;
                        break;
                    }
                } else if (aux->siguiente == NULL) {//------------->insertar al final
                    aux->siguiente = nuevo;
                    nuevo->anterior = aux;
                    break;
                }
            }
            aux = aux->siguiente;
        }

    }
    ret.first = primero;

    return ret;
}

/*
 * Metodo para verificar si es hoja
 * Un nodo hoja no pose apuntadores a otros nodos hacia izquierda o derecha
 */
bool ArbolB::esHoja(NodoB* primero) {
    NodoB* aux = primero;
    while (aux != NULL) {
        cout << "[" << aux->usuario->id << "]->";
        if (aux->izquierda != NULL or aux->derecha != NULL) {
            return false;
        }
        aux = aux->siguiente;
    }
    cout << "Null\n";
    return true;
}

/*Metodo para contar los elementos de una rama*/
int ArbolB::contador(NodoB* primero) {
    int contador = 0;
    NodoB* aux = primero;
    while (aux != NULL) {
        contador++;
        aux = aux->siguiente;
    }
    return contador;
}

//================================Grafo solo del arbol b=====================

void ArbolB::Grafo() {
    string dotFull = "";
    //escribir dot

    dotFull += "digraph G {\n";
    dotFull += "node[shape=record]\n";
    dotFull += "\t\t//Agregar Nodos Rama\n";
    dotFull += GrafoArbolAbb(raiz);
    //agregar conexiones de ramas
    dotFull += "\t\t//Agregar conexiones\n";
    dotFull += GrafoConexionRamas(raiz);

    dotFull += "}";

    //------->escribir archivo
    ofstream file;
    file.open("ArbolUsuarios.dot");
    file << dotFull;
    file.close();

    //------->generar png
    system(("dot -Tpng ArbolUsuarios.dot -o  ArbolUsuarios.png"));

    //------->generar pdf
    system(("dot -Tpdf ArbolUsuarios.dot -o  ArbolUsuarios.pdf"));

    

}

string ArbolB::GrafoArbolAbb(NodoB* rama) {
    string dot = "";
    if (rama != NULL) {
        //agrear rama actual
        dot += GrafoRamas(rama);
        //agregar las ramas siguientes recursivamente
        NodoB*aux = rama;
        while (aux != NULL) {
            if (aux->izquierda != NULL) {
                dot += GrafoArbolAbb(aux->izquierda);
            }
            if (aux->siguiente == NULL) {
                if (aux->derecha != NULL) {
                    dot += GrafoArbolAbb(aux->derecha);
                }
            }
            aux = aux->siguiente;
        }
    }
    return dot;
}

string ArbolB::GrafoRamas(NodoB*rama) {
    string dot = "";
    stringstream auxTXT;
    if (rama != NULL) {
        //============================================agregar rama=================================
        NodoB*aux = rama;
        auxTXT.str("");
        auxTXT << rama;
        dot = dot + "R" + auxTXT.str() + "[label=\"";
        int r = 1;
        while (aux != NULL) {
            if (aux->izquierda != NULL) {
                dot = dot + "<C"  + to_string(r) + ">|";
                r++;
            }
            if (aux->siguiente != NULL) {
                dot = dot + "ID: " + to_string(aux->usuario->id) + "\\n Nick: " + aux->usuario->nick + "|";
            } else {
                dot = dot + "ID: " + to_string(aux->usuario->id) + "\\n Nick: " + aux->usuario->nick;
                if (aux->derecha != NULL) {
                    dot = dot + "|<C" + to_string(r) + ">";
                }
            }
            aux = aux->siguiente;
        }
        dot = dot + "\"];\n";
    }
    return dot;
}

string ArbolB::GrafoConexionRamas(NodoB*rama) {
    string dot = "";
    stringstream auxTXT;
    if (rama != NULL) {
        //============================================agregar rama=================================
        NodoB*aux = rama;
        auxTXT << rama;
        string actual = "R" + auxTXT.str();
        int r = 1;
        while (aux != NULL) {
            if (aux->izquierda != NULL) {
                auxTXT.str("");
                auxTXT << aux->izquierda;
                dot += actual + ":C" + to_string(r) + "->" + "R" + auxTXT.str() + ";\n";
                r++;
                dot += GrafoConexionRamas(aux->izquierda);
            }
            if (aux->siguiente == NULL) {
                if (aux->derecha != NULL) {
                    auxTXT.str("");
                    auxTXT << aux->derecha;
                    dot += actual + ":C" + to_string(r) + "->" + "R" + auxTXT.str() + ";\n";
                    r++;
                    dot += GrafoConexionRamas(aux->derecha);
                }
            }
            aux = aux->siguiente;
        }
    }
    return dot;
}


void ArbolB::agregarTodosLosUsuarios(ListaUsuarios usuarios){
    nodoUsuarios*aux = usuarios.primero;
    while(aux != NULL){
        insertar(aux);
        aux = aux->sig;
        if(aux == usuarios.primero){
            break;
        }
    }
}

bool ArbolB::login(string nick,string password, int id){
    NodoB*aux = raiz;
    while(aux != NULL){
        if(aux->usuario->nick == nick && aux->usuario->password == password && aux->usuario->id == id){
            return true;
        }else if(id < aux->usuario->id){
                aux = aux->izquierda;
        }else if(aux->siguiente != NULL){
            aux = aux->siguiente;
        }else{
            aux = aux->derecha;
        }
    }
    return false;
}

NodoB * ArbolB::buscar(int id){
    NodoB*aux = raiz;
    while(aux != NULL){
        if(aux->usuario->id == id){
            return aux;
        }else if(id < aux->usuario->id){
                aux = aux->izquierda;
        }else if(aux->siguiente != NULL){
            aux = aux->siguiente;
        }else{
            aux = aux->derecha;
        }
    }
    return NULL;
}

void ArbolB::eliminar(int id){
    NodoB*aux = buscar(id);
    if(aux != NULL){
        if(aux->izquierda == NULL && aux->derecha == NULL){
            if(aux->siguiente != NULL){
                aux->siguiente->anterior = aux->anterior;
            }
            if(aux->anterior != NULL){
                aux->anterior->siguiente = aux->siguiente;
            }
            if(aux == raiz){
                raiz = aux->siguiente;
            }
            delete aux;
        }else if(aux->izquierda == NULL && aux->derecha != NULL){
            if(aux->siguiente != NULL){
                aux->siguiente->anterior = aux->anterior;
            }
            if(aux->anterior != NULL){
                aux->anterior->siguiente = aux->siguiente;
            }
            if(aux == raiz){
                raiz = aux->siguiente;
            }
            delete aux;
        }else if(aux->izquierda != NULL && aux->derecha == NULL){
            if(aux->siguiente != NULL){
                aux->siguiente->anterior = aux->anterior;
            }
            if(aux->anterior != NULL){
                aux->anterior->siguiente = aux->siguiente;
            }
            if(aux == raiz){
                raiz = aux->siguiente;
            }
            delete aux;
        }else{
            NodoB*aux2 = aux->siguiente;
            while(aux2->izquierda != NULL){
                aux2 = aux2->izquierda;
            }
            aux->usuario = aux2->usuario;
            if(aux2->siguiente != NULL){
                aux2->siguiente->anterior = aux2->anterior;
            }
            if(aux2->anterior != NULL){
                aux2->anterior->siguiente = aux2->siguiente;
            }
            delete aux2;
        }
    }
}

void ArbolB::insertarCompra(nodoUsuarios*usuario, nodoArticulos*articulo, int cantidad){
    NodoB*aux = buscar(usuario->id);
    if(aux != NULL){
        aux->usuario->compras = insert(aux->usuario->compras, articulo, cantidad);
    }
}


void ArbolB::mostrarVentas(nodoUsuarios*usuario){
    NodoB*aux = buscar(usuario->id);
    if(aux != NULL){
        printTree(aux->usuario->compras,0);
    }
}

string ArbolB::getDatosComoJson(){
    string json = "\"usuarios\":[";
    NodoB*aux = raiz;
    while(aux != NULL){
        json += "{";
        json += "\"nick\": \"" + aux->usuario->nick + "\",";
        json += "\"password\": \"" + aux->usuario->password + "\",";
        json += "\"id\": \"" + to_string(aux->usuario->id) + "\",";
        json += "\"monedas\": \"" + to_string(aux->usuario->monedas) + "\",";
        json += "\"edad\": \"" + to_string(aux->usuario->edad) + "\"";
        json += "}";
        if(aux->siguiente != NULL){
            json += ",";
        }
        aux = aux->siguiente;
    }
    json += "]";
    return json;

}
