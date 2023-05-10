//Kirill Makienko  10-05-23

#include <iostream>
#include<string>
#include <list>
#include<vector>
//#include "MQTTClient.h"
using namespace std;

//Todo
// opciones -m Mensaje, -c Channel, -p IP del servidor

/*a.exe send -p 123.456.789.123 -c Carlos
do while(connection, no se interrumpa por usuario){
input = "Que mensaje desea enviar"
enviar.input()
}
*/

/*a.exe send -p 123.456.789.123 -c Carlos -m hola
*se termina el programa*
}
*/

/*
a.exe subscribe -p 123.456.789.123 -c Carlos 
*En blanco hasta que envien algo*
*/




int main(int argc, char* argv[]) {
    int a;
    string input(argv[1]), optionsString(argv[2]), inputString(argv[3]), options2String(argv[4]),options2String(argv[5]), options3String(argv[6]),options3String(argv[6]);
    cout << argv[1] << endl; //argv[0] es a.exe, o nombredelprograma.exe y argv[1] es el "1er" argumento que se pasa


    if(input == "send"){
       cout << "Va a enviar un mensaje\n";
    }
    else if(input == "subscribe"){
       cout << "Va a suscribir a un hilo\n";
    }
    else{
        cout << "Opcion invalida\n";
        cout << "Terminando programa\n";
    }
    cin >> a; 
    return 0;
}