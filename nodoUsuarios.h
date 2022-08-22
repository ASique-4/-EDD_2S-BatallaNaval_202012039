#ifndef NODOSUSUARIOS_H
#define NODOSUSUARIOS_H
#include <stddef.h>
#include <string>

using namespace std;
class nodoUsuarios {
public:
    std::string nick;
    std::string password;
    int monedas;
    int edad;

    nodoUsuarios*ant;
    nodoUsuarios*sig;
    nodoUsuarios() {
        ant = NULL;
        sig = NULL;
        nick = ' ';
        password = ' ';
        monedas = 0;
        edad = 0;
    }
private:
};
#endif /* NODOSUSUARIOS_H */