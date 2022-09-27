/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/cppFiles/main.cc to edit this template
 */

/*
 * File:   main.cpp
 * Author: angel
 *
 * Created on 13 de agosto de 2022, 13:07
 */

#include "glove/glovehttpserver.hpp"
#include "ListaArticulos.cpp"
#include "ArbolB.cpp"
#include "ListaDeListasMov.cpp"
#include "ColaTutorial.cpp"
#include "CabeceraArticulos.cpp"
#include "ListaMovimientos.cpp"
#include "git/sha256.cpp"
#include <cstdlib>
#include <iostream>
#include "glove/json.hpp"
#include <jsoncpp/json/json.h>
#include "jsoncpp.cpp"
#include <fstream>
#include <chrono>
#include <thread>
#include <string>
#include <vector>


using namespace std;

int stringtoint(string cadena)
{
    int numero = 0;
    for (int i = 0; i < cadena.length(); i++)
    {
        numero = numero * 10 + cadena[i] - '0';
    }
    return numero;
}

char *stringtochar(string s)
{

    char *char_arr;
    string str_obj(s);
    char_arr = &str_obj[0];
    return char_arr;
}

string encriptarSHA256(string cadena)
{
    cadena = stringtochar(cadena);
    SHA2562 sha256;
    return sha256(cadena);
}

void menuEditar(nodoUsuarios *usuarioActivo)
{
    int opcion;
    bool salir = false;
    string nick;
    int edad;
    string password;
    system("clear");
    cout << "Editar usuario" << endl;
    cout << "Nick: " << usuarioActivo->nick << endl;
    cout << "Edad: " << usuarioActivo->edad << endl;
    cout << "Password: " << usuarioActivo->password << endl;

    do
    {
        cout << "================================" << endl;
        cout << "1. Editar nick" << endl;
        cout << "2. Editar edad" << endl;
        cout << "3. Editar password" << endl;
        cout << "4. Volver" << endl;
        cout << "================================" << endl;
        cout << "Ingrese una opcion: ";
        cin >> opcion;

        switch (opcion)
        {
        case 1:
            cout << "Ingrese el nuevo nick: ";
            cin >> nick;
            usuarioActivo->nick = nick;
            cin.get();
            break;
        case 2:
            cout << "Ingrese la nueva edad: ";
            cin >> edad;
            usuarioActivo->edad = edad;
            cin.get();
            break;
        case 3:
            cout << "Ingrese la nueva password: ";
            cin >> password;
            usuarioActivo->password = password;
            cin.get();
            break;
        case 4:
            salir = true;
            break;
        }
    } while (salir);
}

void menuLogin(nodoUsuarios *usuarioActivo, ListaUsuarios usuarios, ColaTutorial tutorial, ListaArticulos articulos)
{
    int opcion;
    bool repetir = true;

    do
    {
        cout << "       ==> Bienvenido " << usuarioActivo->nick << " <==" << endl;
        cout << "=======================================" << endl;
        cout << "1. Editar usuario" << endl;
        cout << "2. Eliminar usuario" << endl;
        cout << "3. Ver tutorial" << endl;
        cout << "4. Ver articulos de la tienda" << endl;
        cout << "5. Realizar movimientos" << endl;
        cout << "6. Mostrar movimientos" << endl;
        cout << "7. Cerrar sesion" << endl;
        cout << "=======================================" << endl;
        cout << endl;
        cout << endl;
        cout << "=>Ingrese una opcion: ";
        cin >> opcion;
        cout << endl;
        cout << endl;
        switch (opcion)
        {
        case 1:

            menuEditar(usuarioActivo);
            break;
        case 2:
        {
            cout << "Eliminar usuario" << endl;
            cout << "¿Esta seguro que desea eliminar el usuario? (s/n): ";
            char respuesta;
            cin >> respuesta;
            if (respuesta == 's')
            {
                usuarios.EliminarUsuario(usuarioActivo);
                repetir = false;
                cout << "Usuario eliminado" << endl;
                cin.get();
                cout << endl;
                cout << endl;
            }
            else
            {
                cout << "Se ha cancelado la eliminacion" << endl;
                cin.get();
                cout << endl;
                cout << endl;
            }
        }
        break;
        case 3:
            cout << "       Ver tutorial" << endl;
            {
                tutorial.Imprimir();
                cin.get();
                cout << endl;
            }
            break;
        case 4:
            cout << "Ver articulos de la tienda" << endl;
            {
                cout << "==========================Monedas: " << usuarioActivo->monedas << endl;
                articulos.Imprimir();
                cin.get();
                cout << endl;
            }
            break;
        case 5:
            cout << "Realizar movimientos" << endl;
            {
                ListaMovimientos *colaMovimientos;
                colaMovimientos = new ListaMovimientos();
                bool repetir = true;
                int i = 1;
                do
                {
                    cout << "Movimiento numero: " << i << endl;
                    cout << "Coordenad en x: ";
                    int x;
                    cin >> x;
                    cout << "Coordenad en y: ";
                    int y;
                    cin >> y;
                    cout << x << " " << y << endl;
                    colaMovimientos->InsertarFinal(x, y);
                    i += 1;
                    cout << "Desea agregar otro movimiento? (s/n): ";
                    char respuesta;
                    cin >> respuesta;
                    if (respuesta == 'n')
                    {
                        cout << "Se han agregado " << i - 1 << " movimientos" << endl;
                        cout << "¿Qué nombre desea ponerle a su movimiento? ";
                        string nombre;
                        cin >> nombre;
                        colaMovimientos->nombre = nombre;

                        cin.get();
                        repetir = false;
                    }
                } while (repetir);

                usuarioActivo->lista.InsertarFinal(colaMovimientos);
                usuarioActivo->monedas += 1;
                cout << usuarioActivo->lista.primero->lista->nombre << endl;
                cout << "Movimientos agregados exitosamente" << endl;
                cin.get();
                cout << endl;
            }
            break;
        case 6:
            cout << "Mostrar movimientos" << endl;
            {
                usuarios.MostrarMovimientos(usuarioActivo);
                cout << "Mostrar movimientos exitosamente" << endl;
                usuarioActivo->lista.CrearGraphviz();
                cin.get();
                cout << endl;
            }
            break;
        case 7:
            cout << "Saliendo al menu principal" << endl;
            cin.get();
            repetir = false;
            break;
        }

    } while (repetir);
}

void login(ListaUsuarios usuarios, ColaTutorial tutorial, ListaArticulos articulos)
{
    system("clear");
    cout << "=======================================" << endl;
    cout << "               LOGIN" << endl;

    cout << "=>Nick: ";
    string nick;
    cin >> nick;
    cout << "=>Password: ";
    string password;
    cin >> password;
    cout << endl;
    cout << endl;
    nodoUsuarios *usuarioActivo = usuarios.BuscarUsuario(nick, encriptarSHA256(password));
    if (usuarioActivo != NULL)
    {

        menuLogin(usuarioActivo, usuarios, tutorial, articulos);
    }
    else
    {
        cout << "Usuario no encontrado :(" << endl;
        cout << endl;
        cout << endl;
    }
}

int atoi(std::string s)
{
    try
    {
        return std::stod(s);
    }
    catch (std::exception &e)
    {
        return 0;
    }
}

static std::string jsonkv(std::string k, std::string v)
{
    /* "k": "v" */
    return "\"" + k + "\": \"" + v + "\"";
}

void cargarArchivos(string archivo, ListaUsuarios usuarios, ListaArticulos articulos, ColaTutorial tutorial, Cabecera cabecera){
    ifstream ifs(archivo);
    Json::Value usuariosObj;
    Json::Reader reader;

    reader.parse(ifs, usuariosObj);
    const Json::Value &usuariosJson = usuariosObj["usuarios"];
    for (int i = 0; i < usuariosJson.size(); i++)
    {
        if (usuarios.BuscarNick(usuariosJson[i]["nick"].asString()) == false)
        {
            usuarios.InsertarFinal(usuariosJson[i]["nick"].asString(), encriptarSHA256(usuariosJson[i]["password"].asString()),
                                    stringtoint(usuariosJson[i]["monedas"].asString()), stringtoint(usuariosJson[i]["edad"].asString()));
        }
    }
    ifstream ifs2(archivo);
    Json::Value articulosObj;
    reader.parse(ifs2, articulosObj);

    const Json::Value &articulosJson = articulosObj["articulos"];
    for (int i = 0; i < articulosJson.size(); i++)
    {

        if (cabecera.Buscar(articulosJson[i]["categoria"].asString()) != true)
        {
            cabecera.InsertarFinal(articulosJson[i]["categoria"].asString());
        }
    }
    for (int i = 0; i < articulosJson.size(); i++)
    {
        articulos.InsertarFinal(articulosJson[i]["id"].asString(), articulosJson[i]["categoria"].asString(),
                                stringtoint(articulosJson[i]["precio"].asString()), articulosJson[i]["nombre"].asString(), articulosJson[i]["src"].asString());
    }
    cabecera.InsertarArticulos(articulos);

    ifstream ifs3(archivo);
    Json::Value tutorialObj;
    reader.parse(ifs3, tutorialObj);
    const Json::Value &tutorialJson = tutorialObj["tutorial"];
    const Json::Value &movimientosJson = tutorialJson["movimientos"];

    tutorial.InsertarFinal(stringtoint(tutorialJson["ancho"].asString()),
                            stringtoint(tutorialJson["alto"].asString()));
    for (int i = 0; i < movimientosJson.size(); i++)
    {
        tutorial.InsertarFinal(stringtoint(movimientosJson[i]["x"].asString()),
                                stringtoint(movimientosJson[i]["y"].asString()));
    }

    ifs.close();
    ifs2.close();
    ifs3.close();

    cout << "Se ha cargado el archivo correctamente" << endl;
    
    
}


class Servidor
{
public:
    Servidor(ListaUsuarios servidorUsuarios, ColaTutorial servidorTutorial, ListaArticulos servidorArticulos, 
            Cabecera servidorCabecera,string servidorRuta, ArbolB servidorArbol)
    {
        
        serverArbol = servidorArbol;
        serverUsuarios = servidorUsuarios;
        serverTutorial = servidorTutorial;
        serverArticulos = servidorArticulos;
        serverCabecera = servidorCabecera;
        ruta = servidorRuta;
    }

    void getUsuarios(GloveHttpRequest &request, GloveHttpResponse &response)
    {
        response.contentType("text/json");
        if(!(ruta == ""))
        {
            
            ifstream ifs(ruta);
            Json::Value usuariosObj;
            Json::Reader reader;

            reader.parse(ifs, usuariosObj);
            const Json::Value &usuariosJson = usuariosObj["usuarios"];
            for (int i = 0; i < usuariosJson.size(); i++)
            {
                if (serverUsuarios.BuscarNick(usuariosJson[i]["nick"].asString()) == false)
                {
                    serverUsuarios.InsertarFinal(usuariosJson[i]["nick"].asString(), encriptarSHA256(usuariosJson[i]["password"].asString()),
                                            stringtoint(usuariosJson[i]["monedas"].asString()), stringtoint(usuariosJson[i]["edad"].asString()));
                }
            }

            serverArbol.agregarTodosLosUsuarios(serverUsuarios);

            ifstream ifs2(ruta);
            Json::Value articulosObj;
            reader.parse(ifs2, articulosObj);

            const Json::Value &articulosJson = articulosObj["articulos"];
            for (int i = 0; i < articulosJson.size(); i++)
            {

                if (serverCabecera.Buscar(articulosJson[i]["categoria"].asString()) != true)
                {
                    serverCabecera.InsertarFinal(articulosJson[i]["categoria"].asString());
                }
            }
            for (int i = 0; i < articulosJson.size(); i++)
            {
                serverArticulos.InsertarFinal(articulosJson[i]["id"].asString(), articulosJson[i]["categoria"].asString(),
                                        stringtoint(articulosJson[i]["precio"].asString()), articulosJson[i]["nombre"].asString(), articulosJson[i]["src"].asString());
            }
            serverCabecera.InsertarArticulos(serverArticulos);

            ifstream ifs3(ruta);
            Json::Value tutorialObj;
            reader.parse(ifs3, tutorialObj);
            const Json::Value &tutorialJson = tutorialObj["tutorial"];
            const Json::Value &movimientosJson = tutorialJson["movimientos"];

            serverTutorial.InsertarFinal(stringtoint(tutorialJson["ancho"].asString()),
                                    stringtoint(tutorialJson["alto"].asString()));
            for (int i = 0; i < movimientosJson.size(); i++)
            {
                serverTutorial.InsertarFinal(stringtoint(movimientosJson[i]["x"].asString()),
                                        stringtoint(movimientosJson[i]["y"].asString()));
            }

            ifs.close();
            ifs2.close();
            ifs3.close();

            cout << "Se ha cargado el archivo correctamente" << endl;
            response << serverUsuarios.getDatosComoJson();
            
        }else{
            response << "{"
                        << "\"error\": \"No se ha cargado ningun archivo\""
                        << "}";
        }
        
    }

    void postRuta(GloveHttpRequest &request, GloveHttpResponse &response)
    {
        ruta = request.special["ruta"];
        std::string json = "{";
        json += jsonkv("ruta", ruta);
        json += "}";
        response << json;
    }

    void getUsuario(GloveHttpRequest &request, GloveHttpResponse &response){

        response.contentType("text/json");
        if(request.special["nick"] != "" && request.special["password"] != ""){
            if(serverArbol.login(request.special["nick"], request.special["password"])){
                response << "{"
                        << "\"status\": \"ok\","

                 << "\"usuario\": ["
                        << jsonkv("nick", serverArbol.buscar(stringtoint(request.special["id"]))->usuario->nick) << ","
                        << jsonkv("password", serverArbol.buscar(stringtoint(request.special["id"]))->usuario->password) << ","
                        << jsonkv("monedas", to_string(serverArbol.buscar(stringtoint(request.special["id"]))->usuario->monedas))   << ","
                        << jsonkv("edad", to_string(serverArbol.buscar(stringtoint(request.special["id"]))->usuario->edad))  << ","
                        << jsonkv("id", to_string(serverArbol.buscar(stringtoint(request.special["id"]))->usuario->id))
                        << "]"
                 << "}";
            }else{
                response << "{"
                        << jsonkv("error", "El usuario no existe")
                        << "}";
            }
        }
    }

    void postCrearUsuario(GloveHttpRequest &request, GloveHttpResponse &response)
    {
        response.contentType("text/json");
        if(request.special["nick"] != "" && request.special["password"] != "" && request.special["edad"] != ""){
            if(serverArbol.buscar(stringtoint(request.special["id"])) == NULL){
                nodoUsuarios *nuevo = new nodoUsuarios();
                nuevo->nick = request.special["nick"];
                nuevo->password = encriptarSHA256(request.special["password"]);
                nuevo->monedas = 0;
                nuevo->edad = stringtoint(request.special["edad"]);

                serverArbol.insertar(nuevo);
                //serverUsuarios.InsertarFinal(request.special["nick"],encriptarSHA256(request.special["password"]),0,stringtoint(request.special["edad"]));
                response << "{"
                        << jsonkv("nick", request.special["nick"])
                        << "}";
            }else{
                response << "{"
                        << jsonkv("error", "El usuario ya existe")
                        << "}";
            }
        }
    }

    void postEliminarUsuario(GloveHttpRequest &request, GloveHttpResponse &response)
    {
        response.contentType("text/json");
        if(request.special["id"] != ""){
            if(serverArbol.buscar(stringtoint(request.special["id"])) != NULL){
                serverArbol.eliminar(stringtoint(request.special["id"]));
                //serverUsuarios.EliminarUsuario(serverUsuarios.BuscarUsuario(request.special["nick"],(request.special["password"])));
                
                response << "{"
                        << jsonkv("nick", request.special["nick"])
                        << jsonkv("status", "ok")
                        << "}";
            }else{
                response << "{"
                        << jsonkv("status", "El usuario no existe")
                        << "}";
            }
        }
    }

    void postModificarUsuario(GloveHttpRequest &request, GloveHttpResponse &response)
    {
        response.contentType("text/json");
        if(request.special["id"] != ""){
            if(serverArbol.buscar(stringtoint(request.special["id"])) != NULL){

                nodoUsuarios* aux = serverArbol.buscar(stringtoint(request.special["id"]))->usuario;
                aux->nick = request.special["newNick"];
                aux->password = encriptarSHA256(request.special["newPassword"]);
                aux->edad = stringtoint(request.special["newEdad"]);

                response << "{"
                        << jsonkv("status", "ok")
                        << "usuario: ["
                        << jsonkv("nick", aux->nick) << ","
                        << jsonkv("password", encriptarSHA256(aux->password)) << ","
                        << jsonkv("edad", to_string(aux->edad)) << ","
                        << jsonkv("id", to_string(aux->id)) << ","
                        << jsonkv("monedas", to_string(aux->monedas))
                        << "]"
                        << "}";

                // nodoUsuarios *tmpUsuario = serverUsuarios.BuscarUsuario(request.special["nick"],(request.special["password"]));
                // tmpUsuario->edad = stringtoint(request.special["newEdad"]);
                // tmpUsuario->nick = (request.special["newNick"]);
                // tmpUsuario->password = encriptarSHA256(request.special["newPassword"]);
                // response << "{"
                //         << jsonkv("status", "ok")
                //         << "usuario: ["
                //         << jsonkv("nick", tmpUsuario->nick) << ","
                //         << jsonkv("password", encriptarSHA256(tmpUsuario->password)) << ","
                //         << jsonkv("edad", to_string(tmpUsuario->edad))
                //         << "]"
                //         << "}";
            }else{
                response << "{"
                        << jsonkv("error", "El usuario no existe")
                        << "}";
            }
        }
    }

    void getTienda(GloveHttpRequest &request, GloveHttpResponse &response){
        response.contentType("text/json");
        response << "{"
                << serverCabecera.getArticulosComoJson()
                << "}";
    }

    void postCompra(GloveHttpRequest &request, GloveHttpResponse &response){
        response.contentType("text/json");
        if(request.special["nick"] != "" && request.special["password"] != "" && request.special["id"] != ""){
            if(serverArbol.buscar(stringtoint(request.special["id"])) != NULL){
                nodoUsuarios *tmpUsuario = serverArbol.buscar(stringtoint(request.special["id"]))->usuario;
                nodoArticulos *tmpArticulo = serverArticulos.getArticulo(request.special["id"]);
                if(tmpArticulo != NULL){
                    int tmp = stringtoint(request.special["cantidad"]);
                    serverArbol.insertarCompra(tmpUsuario, tmpArticulo, tmp);
                    serverArbol.buscar(stringtoint(request.special["id"]))->usuario->monedas -= tmpArticulo->precio * tmp;
                    response << "{"
                            << jsonkv("status", "ok")   << ","
                            << jsonkv("nick", tmpUsuario->nick) << ","
                            << jsonkv("monedas", to_string(tmpUsuario->monedas))
                            << "}";
                }else{
                    response << "{"
                            << jsonkv("status", "El articulo no existe")
                            << "}";
                }
            }else{
                response << "{"
                        << jsonkv("status", "El usuario no existe")
                        << "}";
            }
        }
    }

    void getGraficar(GloveHttpRequest &request, GloveHttpResponse &response){
        if(request.special["estructura"] == "arbol"){
            serverArbol.Grafo();
            response << "{"
                    << jsonkv("status", "ok") << ","
                    << jsonkv("url", "Fase2/Servidor/Pruebas.png")
                    << "}";
        } else if (request.special["estructura"] == "compras" and request.special["id"] != ""){
            cout << "Graficando compras de " << request.special["nick"] << endl;
            serverArbol.mostrarVentas(serverArbol.buscar(stringtoint(request.special["id"]))->usuario);
            response << "{"
                    << jsonkv("status", "ok") << ","
                    << jsonkv("url", "Fase2/Servidor/Compras.png")
                    << "}";
        } else {
            response.contentType("text/json");
            response << "{"
                    << jsonkv("status", "error") << ","
                    << jsonkv("error", "Estructura no encontrada")
                    << "}";
        }
        

    }

private:
    ListaUsuarios serverUsuarios;
    ListaArticulos serverArticulos;
    ColaTutorial serverTutorial;
    Cabecera serverCabecera;
    string ruta;
    ArbolB serverArbol;
};

void menu(ListaUsuarios usuarios, ListaArticulos articulos, ColaTutorial tutorial, Cabecera cabecera)
{

    int opcion;
    string archivo;
    bool repetir = true;
    

    do
    {

        // Texto del menú que se verá cada vez
        cout << "=======================================" << endl;
        cout << "           Menu de Opciones" << endl;
        cout << "1. Carga Masiva" << endl;
        cout << "2. Registrar Usuario" << endl;
        cout << "3. Login" << endl;
        cout << "4. Reportes" << endl;
        cout << "0. Salir" << endl;
        cout << "=======================================" << endl;
        cout << "   Ingrese una opcion: ";
        cin >> opcion;

        switch (opcion)
        {
        case 1:

            // Lista de instrucciones de la opción 1
            cout << "=>Elija un archivo JSON para cargar: " << endl;
            cin >> archivo;

            {
                ifstream ifs(archivo);
                Json::Value usuariosObj;
                Json::Reader reader;

                reader.parse(ifs, usuariosObj);
                const Json::Value &usuariosJson = usuariosObj["usuarios"];
                for (int i = 0; i < usuariosJson.size(); i++)
                {
                    if (usuarios.BuscarNick(usuariosJson[i]["nick"].asString()) == false)
                    {
                        usuarios.InsertarFinal(usuariosJson[i]["nick"].asString(), encriptarSHA256(usuariosJson[i]["password"].asString()),
                                               stringtoint(usuariosJson[i]["monedas"].asString()), stringtoint(usuariosJson[i]["edad"].asString()));
                    }
                }

                ifstream ifs2(archivo);
                Json::Value articulosObj;
                reader.parse(ifs2, articulosObj);

                const Json::Value &articulosJson = articulosObj["articulos"];
                for (int i = 0; i < articulosJson.size(); i++)
                {

                    if (cabecera.Buscar(articulosJson[i]["categoria"].asString()) != true)
                    {
                        cabecera.InsertarFinal(articulosJson[i]["categoria"].asString());
                    }
                }
                for (int i = 0; i < articulosJson.size(); i++)
                {
                    articulos.InsertarFinal(articulosJson[i]["id"].asString(), articulosJson[i]["categoria"].asString(),
                                            stringtoint(articulosJson[i]["precio"].asString()), articulosJson[i]["nombre"].asString(), articulosJson[i]["src"].asString());
                }
                cabecera.InsertarArticulos(articulos);

                ifstream ifs3(archivo);
                Json::Value tutorialObj;
                reader.parse(ifs3, tutorialObj);
                const Json::Value &tutorialJson = tutorialObj["tutorial"];
                const Json::Value &movimientosJson = tutorialJson["movimientos"];

                tutorial.InsertarFinal(stringtoint(tutorialJson["ancho"].asString()),
                                       stringtoint(tutorialJson["alto"].asString()));
                for (int i = 0; i < movimientosJson.size(); i++)
                {
                    tutorial.InsertarFinal(stringtoint(movimientosJson[i]["x"].asString()),
                                           stringtoint(movimientosJson[i]["y"].asString()));
                }

                ifs.close();
                ifs2.close();
                ifs3.close();
                cout << endl;
                cout << endl;
                cout << "Se ha cargado el archivo correctamente" << endl;
                

            }
            
            break;

        case 2:
            // Lista de instrucciones de la opción 2

            {

                string nick;
                string password;
                int monedas;
                int edad;
                cout << "Registrar usuario" << endl;
                cout << "=>Nick: ";
                cin >> nick;
                cout << "=>Password: ";
                cin >> password;

                cout << "=>Edad: ";
                cin >> edad;
                if (usuarios.BuscarNick(nick) == false)
                {
                    usuarios.InsertarFinal(nick, encriptarSHA256(password), 0, edad);
                    cout << "Usuario registrado" << endl;
                }else{
                    cout << "Ya existe un usuario con este nick" << endl;
                    cin.get();
                }

                cin.get();
                cout << endl;
                cout << endl;
            }

            break;

        case 3:
            // Lista de instrucciones de la opción 3
            login(usuarios, tutorial, articulos);
            break;

        case 4:
            // Lista de instrucciones de la opción 4
            {
                int i;
                bool repetir1 = true;
                do
                {
                    cout << "=======================================" << endl;
                    cout << "           Reportes" << endl;
                    cout << "1. Reporte de usuarios" << endl;
                    cout << "2. Reporte de articulos" << endl;
                    cout << "3. Reporte de tutorial" << endl;
                    cout << "0. Salir" << endl;
                    cout << "=======================================" << endl;
                    cout << "   Ingrese una opcion: ";
                    cin >> i;
                    switch (i)
                    {
                    case 1:
                        // Lista de instrucciones de la opción 1
                        {
                            int i;
                            bool repetir2 = false;
                            cout << "=======================================" << endl;
                            cout << "1. Ordenar de maenra descendente" << endl;
                            cout << "2. Ordenar de manera ascendente" << endl;
                            cout << "0. Salir" << endl;
                            cout << "=======================================" << endl;
                            cin >> i;
                            do
                            {
                                switch (i)
                                {
                                case 1:
                                    usuarios.OrdenamientoDescendente();
                                    usuarios.Imprimir();
                                    usuarios.CrearGraphviz();
                                    cout << endl;
                                    cout << endl;
                                    break;
                                case 2:
                                    usuarios.OrdenamientoAscendente();
                                    usuarios.Imprimir();
                                    usuarios.CrearGraphviz();
                                    cin.get();
                                    cout << endl;
                                    cout << endl;
                                    break;
                                case 0:
                                    repetir2 = false;
                                    break;
                                default:
                                    cin.get();
                                    cout << "Opcion no valida" << endl;
                                    break;
                                }
                            } while (repetir2);
                        }
                        break;
                    case 2:
                        // Lista de instrucciones de la opción 2
                        {
                            int i;
                            bool repetir2 = false;
                            cout << "=======================================" << endl;
                            cout << "1. Ordenar de maenra descendente" << endl;
                            cout << "2. Ordenar de manera ascendente" << endl;
                            cout << "0. Salir" << endl;
                            cout << "=======================================" << endl;
                            cin >> i;
                            do
                            {
                                switch (i)
                                {
                                case 1:
                                    articulos.OrdenamientoDescendente();
                                    articulos.Imprimir();
                                    cabecera.CrearGraphviz();
                                    cout << endl;
                                    cout << endl;
                                    break;
                                case 2:
                                    articulos.OrdenamientoAscendente();
                                    articulos.Imprimir();
                                    cabecera.CrearGraphviz();
                                    cout << endl;
                                    cout << endl;
                                    break;
                                case 0:
                                    repetir2 = false;
                                    break;
                                default:
                                    cout << "Opcion no valida" << endl;
                                    cout << endl;
                                    break;
                                }
                                cin.get();
                            } while (repetir2);
                        }
                        break;
                    case 3:
                        // Lista de instrucciones de la opción 3
                        tutorial.Imprimir();
                        tutorial.CrearGraphviz();
                        break;
                    case 0:
                        // Lista de instrucciones de la opción 0
                        repetir1 = false;
                        break;
                    }
                } while (repetir1);
            }
            break;

        case 0:
            repetir = false;
            break;
        }
    } while (repetir);
}


int main(int argc, char **argv)
{
    ListaUsuarios usuarios;
    ListaArticulos articulos;
    ColaTutorial tutorial;
    Cabecera cabecera;
    ArbolB arbol;
    string archivo = "";
    //menu(usuarios, articulos, tutorial, cabecera);
    usuarios.InsertarFinal("EDD", encriptarSHA256("edd123"), 0, 50);
    cout << (encriptarSHA256("edd123")) << endl;
    Servidor API(usuarios,tutorial,articulos,cabecera,archivo,arbol);
    GloveHttpServer serv(8080, "", 2048);
    serv.compression("gzip, deflate");
    namespace ph = std::placeholders;
    serv.addRest("/Cargar/$ruta", 1,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::getUsuarios, &API, ph::_1, ph::_2),
                std::bind(&Servidor::postRuta, &API, ph::_1, ph::_2));
    serv.addRest("/ObtenerUsuario/$nick/$password", 2,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::getUsuario, &API, ph::_1, ph::_2));  
    serv.addRest("/EliminarUsuario/$id", 2,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::postEliminarUsuario, &API, ph::_1, ph::_2));  
    serv.addRest("/CrearUsuario/$nick/$password/$edad/", 3,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::postCrearUsuario, &API, ph::_1, ph::_2));
    serv.addRest("/ModificarUsuario/$id/$newNick/$newPassword/$newEdad", 3,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::postModificarUsuario, &API, ph::_1, ph::_2));
    serv.addRest("/ObtenerTienda/", 0,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::getTienda, &API, ph::_1, ph::_2));
    serv.addRest("/Graficar/$estructura/$id", 1,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::getGraficar, &API, ph::_1, ph::_2));
    serv.addRest("/Comprar/$nick/$password/$id/$cantidad/$total", 1,
                GloveHttpServer::jsonApiErrorCall,
                std::bind(&Servidor::postCompra, &API, ph::_1, ph::_2));
    std::cout << "Servidor en Ejecucion" << std::endl;
    while (1)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    std::cout << "TEST" << std::endl;

    
    return 0;
}

