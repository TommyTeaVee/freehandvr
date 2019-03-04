#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <iostream>
#include <string>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

struct info
{
	int camera : 5;
	int color : 3; //color1, or color2, or hand (1, 2, 3)
	char lowerHSV[8]; //literally only need 8 bytes to store it for the later programs
};

int countCameras();

int calibrate(info *data);


