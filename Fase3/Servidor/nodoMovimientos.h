#ifndef NODOMOVIMIENTOS_H
#define NODOMOVIMIENTOS_H
#include <stddef.h>
#include <string>

using namespace std;
class nodoMovimientos {
public:
    int x;
    int y;
    

    nodoMovimientos*sig;
    nodoMovimientos*ant;
    nodoMovimientos() {
        sig = NULL;
        ant = NULL;
        x = 0;
        y = 0;
    }
    void InsertarFinal(int x, int y);
private:
};
#endif /* NODOMOVIMIENTOS_H */
