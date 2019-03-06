#include "calibration.h"
//write the hsv data to a file in the following format (file will be the whichOne pointer, will improve that later)
//File content:
//h
//s
//v

void writeData(int h, int s, int v, const char *filename)
{
	ofstream dataFile;
	dataFile.open(filename);
	dataFile << h << "\n" << s << "\n" << v;
	dataFile.close();
	return;
}