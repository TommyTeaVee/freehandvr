#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <fstream>

using namespace std;
using namespace cv;

//possible strings to show during the gui calibration
const char * const COLOR1STR = "Calibration for Color 1";
const char * const COLOR2STR = "Calibration for Color 2";
const char * const HANDSTR = "Calibration for Hand";

struct info
{
	int camera : 5; //cap at 15
	int color : 3; //color1, or color2, or hand - 1, 2, 3
	char lowerHSV[8]; //literally only need 8 bytes to store it for the later programs
};

extern inline int countCameras();

int calibrate(info *data, const char *whichOne);

void writeData(int h, int s, int v, const char *filename);


