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

//window name
const char * const WINDOWNAME = "FreeHandVR Calibration";

//instruction strings
const char * const INSTRUCTION1 = "Adjust the Values";
const char * const INSTRUCTION2 = "until you see an Optimal Circle ->";
const char * const INSTRUCTION3 = "ESC - exit";
const char * const INSTRUCTION4 = "N - next cam";
const char * const INSTRUCTION5 = "B - prev cam";
const char * const INSTRUCTION6 = "Enter - confirm values";
const char * const INSTRUCTION7 = "Avoid Balls of Similar Colors";

//possible filenames
const char * const FILENAME1 = "color1";
const char * const FILENAME2 = "color2";
const char * const FILENAME3 = "hand";

struct info
{
	int camera : 5; //cap at 15
	int color : 3; //color1, or color2, or hand - 1, 2, 3
};

extern inline int countCameras();

extern inline int processCalibrate(info *data, const char* display, int flag);

int calibrate(info *data, const char *whichOne, int flag);

void writeData(int h, int s, int v, int cam, const char *filename);

void provideBaseValues(int &lowh, int &lows, int &lowv, int flag);


