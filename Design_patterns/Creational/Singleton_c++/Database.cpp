#include "Database.h"


Database Database::dbInstance;

Database::Database()
{
	dbInstance.connectionStatus = true;
	std::cout << "Database instance is created !\n" << std::endl;
};

Database::~Database()
{
	std::cout << "Database instance is destroyed !\n" << std::endl;
};

Database& Database::getInstanceOfDb()
{
	return dbInstance;
}

void Database::isDbConnected() const {

	bool tempConnectionStatus = dbInstance.connectionStatus;
	if (tempConnectionStatus == true) {
		std::cout << "Database instance is connected !\n" << std::endl;
	}
	else {
		std::cout << "Database instance is not connected !\n" << std::endl;
	}
}