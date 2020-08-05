#include <iostream>
#include <windows.h>

using namespace std;

int main(int argc, char *argv[])
{
    cout << "For proper installation of pygame, the following conditions must be satisfied:" << endl;
    cout << "1. Your system must have one of the latest versions of python and pip installed" << endl;
    cout << "2. Your system must be connected to a stable internet connection" << endl << endl;
    
    cout << "Trying to install pygame" << endl;
    system("pip install pygame");

    cout << "You can close the window now";
    while(1);

    return 0;
}