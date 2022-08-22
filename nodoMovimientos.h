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
    nodoMovimientos() {
        sig = NULL;
        x = 0;
        y = 0;
    }
private:
};
#endif /* NODOMOVIMIENTOS_H */