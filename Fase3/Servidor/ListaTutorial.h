#ifndef LISTATUTORIAL_H
#define LISTATUTORIAL_H

#include "nodoTutorial.h"

#include <iostream>
using namespace std;

class ColaTutorial {
public:
    nodoTutorial*Inicio;
    nodoTutorial*Ultimo;

    ColaTutorial() {
        Inicio = NULL;
        Ultimo = NULL;
    }
    void InsertarFinal(int x, int y);
    void Imprimir();
    void CrearGraphviz();
    string getTutorialComoJson();
private:
};

#endif /* LISTATUTORIAL_H */