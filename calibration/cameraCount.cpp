#include "calibration.h"

int countCameras()
{
	int index = 0;
	//index will be amount of cameras possible
	//capped at 15
	for (int i = 0; i < 15; i++)
	{
		VideoCapture source(index);
		if (!source.isOpened())
		{
			break;
		}
		index++;
		source.release();
	}
	return index;
}