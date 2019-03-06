// calibration.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
//REMEMBER TO CHECK FOR THE EDGE CASES AND ERRORS

#include "calibration.h"

int main()
{
	//getting camera count
	int numCams = countCameras();
	info *color1 = new info;
	info *color2 = new info;
	info *hand = new info;
	//initialize camera values
	color1->camera = 0;
	color2->camera = 0;
	hand->camera = 0;
	calibrate(color1);
	//cleanup
	delete color1;
	delete color2;
	delete hand;
	color1 = 0;
	color2 = 0;
	hand = 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
