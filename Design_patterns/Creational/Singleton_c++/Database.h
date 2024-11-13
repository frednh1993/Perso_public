#pragma once
#include <iostream>


class Database
{
public:
	// Methods :
	static Database& getInstanceOfDb();
	void isDbConnected() const;
	~Database();

private:
	// Attributes :
	static Database dbInstance;
	bool connectionStatus = false;

	// Methods :
	Database();
};

