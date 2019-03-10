#include "calibration.h"

void provideBaseValues(int &lowh, int &lows, int &lowv, int flag) // default (0) is red, 1 is orange, 2 is yellow, 3 is green, 4 is blue, 5 is purple
{
	//just some basic base values, users still have to manually adjust probably
	switch (flag)
	{
		case 1:
			lowh = 0;
			lowv = 83;
			lows = 118;
			break;
		case 2:
			lowh = 27;
			lowv = 83;
			lows = 118;
			break;
		case 3:
			lowh = 22;
			lowv = 82;
			lows = 66;
			break;
		case 4:
			lowh = 102;
			lows = 163;
			lowv = 73;
			break;
		case 5:
			lowh = 113;
			lows = 124;
			lowv = 44;
			break;
		default:
			lowh = 170;
			lows = 70;
			lowv = 50;
			break;
	}
	return;
}