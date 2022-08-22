#ifndef NODOTUTORIAL_H
#define NODOTUTORIAL_H
#include <stddef.h>
#include <string>
#include "ListaMovimientos.h"

using namespace std;
class nodoTutorial {
public:
    int x;
    int y;

    nodoTutorial*sig;
    nodoTutorial() {
        sig = NULL;
        x = 0;
        y = 0;
    }
private:
};
#endif /* NODOTUTORIAL_H */