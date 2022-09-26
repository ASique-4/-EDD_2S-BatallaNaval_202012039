/**
 * \file
 * \brief A simple tree implementation using nodes
 *
 * \todo update code to use C++ STL library features and OO structure
 * \warning This program is a poor implementation and does not utilize any of
 * the C++ STL features.
 */
#include <algorithm>
#include <iostream>
#include <queue>
#include <fstream>
#include "nodoArticulos.h"

typedef struct node {
    nodoArticulos *data;
    int height;
    int cantidad;
    struct node *left;
    struct node *right;
} node;

/** Create and return a new Node */
node *createNode(nodoArticulos *data, int cantidad) {
    node *nn = new node();
    nn->data = data;
    nn->height = 0;
    nn->cantidad = cantidad;
    nn->left = NULL;
    nn->right = NULL;
    return nn;
}

/** Returns height of tree */
int height(node *root) {
    if (root == NULL)
        return 0;
    return 1 + std::max(height(root->left), height(root->right));
}

/** Returns difference between height of left and right subtree */
int getBalance(node *root) { return height(root->left) - height(root->right); }

/** Returns Node after Right Rotation */
node *rightRotate(node *root) {
    node *t = root->left;
    node *u = t->right;
    t->right = root;
    root->left = u;
    return t;
}

/** Returns Node after Left Rotation */
node *leftRotate(node *root) {
    node *t = root->right;
    node *u = t->left;
    t->left = root;
    root->right = u;
    return t;
}

/** Returns node with minimum value in the tree */
node *minValue(node *root) {
    if (root->left == NULL)
        return root;
    return minValue(root->left);
}

/** Balanced Insertion */
node *insert(node *root, nodoArticulos*item,int cantidad) {
    node *nn = createNode(item,cantidad);
    if (root == NULL)
        return nn;
    if (item->precio < root->data->precio)
        root->left = insert(root->left, item,cantidad);
    else
        root->right = insert(root->right, item,cantidad);
    int b = getBalance(root);
    if (b > 1) {
        if (getBalance(root->left) < 0)
            root->left = leftRotate(root->left);  // Left-Right Case
        return rightRotate(root);                 // Left-Left Case
    } else if (b < -1) {
        if (getBalance(root->right) > 0)
            root->right = rightRotate(root->right);  // Right-Left Case
        return leftRotate(root);                     // Right-Right Case
    }
    return root;
}

/** Balanced Deletion */
node *deleteNode(node *root, int key) {
    if (root == NULL)
        return root;
    if (key < root->data->precio)
        root->left = deleteNode(root->left, key);
    else if (key > root->data->precio)
        root->right = deleteNode(root->right, key);

    else {
        // Node to be deleted is leaf node or have only one Child
        if (!root->right) {
            node *temp = root->left;
            delete (root);
            root = NULL;
            return temp;
        } else if (!root->left) {
            node *temp = root->right;
            delete (root);
            root = NULL;
            return temp;
        }
        // Node to be deleted have both left and right subtrees
        node *temp = minValue(root->right);
        root->data->precio = temp->data->precio;
        root->right = deleteNode(root->right, temp->data->precio);
    }
    // Balancing Tree after deletion
    return root;
}

/** LevelOrder (Breadth First Search) */
void levelOrder(node *root) {
    std::queue<node *> q;
    q.push(root);
    while (!q.empty()) {
        root = q.front();
        std::cout << root->data->precio << " ";
        q.pop();
        if (root->left)
            q.push(root->left);
        if (root->right)
            q.push(root->right);
    }
}

/** Graphical Representation of Tree whit graphviz whit precio,id and nombre*/
void printTree(node *root, int space) {
    string dot = "digraph G {";
    if (root == NULL)
        return;
    std::queue<node *> q;
    q.push(root);
    while (!q.empty()) {
        root = q.front();
        q.pop();
        if (root->left) {
            q.push(root->left);
            dot += "\"" + root->data->id + "\"" +"[label=\" ID: " + root->data->id + "\nNombre: " + root->data->nombre + "\nCantidad: " + to_string(root->cantidad) +"\"]";
            dot += "\"" +root->left->data->id + "\"" +"[label=\" ID: " + root->left->data->id + "\nNombre: " + root->left->data->nombre + "\nCantidad: " + to_string(root->left->cantidad) + " \"]";
            dot += "\"" +(root->data->id) + "\"" +"->" +
                   "\"" +(root->left->data->id) + "\"" +";";
        }
        if (root->right) {
            q.push(root->right);
            dot += "\"" +root->data->id + "\"" +"[label=\" ID: " + root->data->id + "\nNombre: " + root->data->nombre + "\nCantidad: " + to_string(root->cantidad) + "\"]";
            dot += "\"" +root->right->data->id + "\"" +"[label=\" ID: " + root->right->data->id + "\nNombre: " + root->right->data->nombre + "\nCantidad: " + to_string(root->right->cantidad) + "\"]";
            dot += "\"" +(root->data->id) +"\"" + "->" +"\"" +
                   (root->right->data->id) + "\"" +";";
        }
    }
    dot += "}";
    std::cout << dot << std::endl;
    ofstream archivo;
    archivo.open("Compras.dot");
    archivo << dot;
    archivo.close();
    system("dot -Tpng Compras.dot -o Compras.png");
}


// int main(int argc, char const *argv[])
// {
//     node *root = NULL;
//     nodoArticulos *articulo = new nodoArticulos();
//     articulo->id = "1";
//     articulo->nombre = "Articulo 1";
//     articulo->precio = 1;
//     root = insert(root, articulo,1);
//     articulo = new nodoArticulos();
//     articulo->id = "2";
//     articulo->nombre = "Articulo 2";
//     articulo->precio = 2;
//     root = insert(root, articulo,2);
//     articulo = new nodoArticulos();
//     articulo->id = "3";
//     articulo->nombre = "Articulo 3";
//     articulo->precio = 3;
//     root = insert(root, articulo,5);
//     articulo = new nodoArticulos();
//     articulo->id = "4";
//     articulo->nombre = "Articulo 4";
//     articulo->precio = 4;
//     root = insert(root, articulo,4);
//     articulo = new nodoArticulos();
//     articulo->id = "5";
//     articulo->nombre = "Articulo 5";
//     articulo->precio = 5;
//     root = insert(root, articulo,9);
//     printTree(root,0);
//     return 0;
// }


