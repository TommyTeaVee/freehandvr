// calibration.cpp : This file contains the 'main' function. Program execution begins and ends here.
//
//REMEMBER TO CHECK FOR THE EDGE CASES AND ERRORS

#include "calibration.h"

int cam = 0; //cam variable will allow to switch cameras
int numCams;

int main()
{
	int cont = 1; // check if continue the calibration process
	//getting camera count
	numCams = countCameras();
	info *color1 = new info;
	info *color2 = new info;
	info *hand = new info;
	//initialize camera values
	color1->camera = 0;
	color2->camera = 0;
	hand->camera = 0;
	//for color1
	if (cont)
	{
		cont = processCalibrate(color1, COLOR1STR);
	}
	//for color2
	if (cont)
	{
		cont = processCalibrate(color2, COLOR2STR);
	}
	//for hand
	if (cont)
	{
		cont = processCalibrate(hand, HANDSTR);
	}
	//cleanup
	delete color1;
	delete color2;
	delete hand;
	color1 = 0;
	color2 = 0;
	hand = 0;
	return 0;
}

inline int processCalibrate(info *data, const char* display) //return 1 if just go on, if returns 0, means user wants to exit, this function is to aid with camera, continue, switching, etc. processes
{
	//for switching cameras, remember to properly cap
	int retValue = 4; //set to 4 to prime the loop
	while (retValue == 4)
	{
		retValue = calibrate(data, display);
		if (retValue == 0)
		{
			break;
		}
		if (retValue == 1)
		{
			data->camera = ((data->camera + 1) == numCams) ? 0 : (data->camera + 1);
			retValue = 4;
		}
		if (retValue == 2)
		{
			data->camera = ((data->camera - 1) == -1) ? (numCams - 1) : (data->camera - 1);
			retValue = 4;
		}
		if (retValue == 3)
		{
			break;
		}
	}
	return (retValue == 0) ? 0 : 1;

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
