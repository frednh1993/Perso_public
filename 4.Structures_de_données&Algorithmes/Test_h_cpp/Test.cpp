#include "Test.h"

class Test
{
private:
	int Counter;

public:
	Test()
	{
		Counter = 100;
	}

	void Fct()
	{
		std::cout << Counter;
	}
};
