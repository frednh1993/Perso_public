// Singleton_c++.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "Database.h"
#include <iostream>


int main()
{
	std::cout << "Start of main !\n";

	Database& dbRef = Database::getInstanceOfDb();
	dbRef.isDbConnected();

	std::cout << "End of main ! \n";
}


