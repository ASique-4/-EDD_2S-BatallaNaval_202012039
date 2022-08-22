#ifndef NODOARTICULOS_H
#define NODOARTICULOS_H
#include <stddef.h>
#include <string>

using namespace std;
class nodoArticulos {
public:
    int id;
    string categoria;
    int precio;
    string nombre;
    string src;
    nodoArticulos*sig;

    nodoArticulos() {
        sig = NULL;
        id = 0;
        categoria = ' ';
        precio = 0;
        nombre = ' ';
        src = ' ';
    }
private:
};
#endif /* NODOARTICULOS_H */