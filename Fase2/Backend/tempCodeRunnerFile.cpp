usuarios.InsertarFinal("EDD", encriptarSHA256("edd123"), 0, 50);
    usuarios.InsertarFinal("EDD2", encriptarSHA256("edd123"), 0, 10);
    usuarios.InsertarFinal("EDD3", encriptarSHA256("edd123"), 0, 20);
    usuarios.InsertarFinal("EDD4", encriptarSHA256("edd123"), 0, 7);
    usuarios.InsertarFinal("EDD5", encriptarSHA256("edd123"), 0, 9);
    usuarios.InsertarFinal("EDD6", encriptarSHA256("edd123"), 0, 14);
    usuarios.Imprimir();

    arbol.insertar(usuarios.BuscarUsuario("EDD", encriptarSHA256("edd123")));
    arbol.insertar(usuarios.BuscarUsuario("EDD2", encriptarSHA256("edd123")));
    arbol.insertar(usuarios.BuscarUsuario("EDD3", encriptarSHA256("edd123")));
    arbol.insertar(usuarios.BuscarUsuario("EDD4", encriptarSHA256("edd123")));
    arbol.insertar(usuarios.BuscarUsuario("EDD5", encriptarSHA256("edd123")));
    arbol.insertar(usuarios.BuscarUsuario("EDD6", encriptarSHA256("edd123")));
    arbol.Grafo();