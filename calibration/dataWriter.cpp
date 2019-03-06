#include "calibration.h"
//write the hsv data to a file in the following format (file will be the whichOne pointer, will improve that later)
//File content:
//camera num
//h
//s
//v

void writeData(int h, int s, int v, int cam, const char *filename)
{
	ofstream dataFile;
	dataFile.open(filename);
	dataFile << cam << "\n" << h << "\n" << s << "\n" << v;
	dataFile.close();
	return;
}