#include "calibration.h"

int calibrate(info *data) //return 1 to stop the same interface from repeating
{
	UMat mainImage, hsvImage, thresholdedImage, combinedView;
	int cont = 1; //check if continue
	VideoCapture source(data->camera); //start camera from camera number defined in structs
	int lowh = 90;
	int lows = 170;
	int lowv = 70;
	int highh = 179;
	int highs = 255;
	int highv = 255;
	namedWindow("Calibration", CV_WINDOW_AUTOSIZE); //create calibration window
	//Create trackbars, usually low changing values is sufficient
	cvCreateTrackbar("LowH", "Calibration", &lowh, 179); //Hue (0 - 179)
	cvCreateTrackbar("LowS", "Calibration", &lows, 255); //Saturation (0 - 255)
	cvCreateTrackbar("LowV", "Calibration", &lowv, 255); //Value (0 - 255)
	while (cont)
	{
		source.read(mainImage);
		//creating HSV image
		cvtColor(mainImage, hsvImage, COLOR_BGR2HSV);
		inRange(hsvImage, Scalar(lowh, lows, lowv), Scalar(highh, highs, highv), thresholdedImage);
		//morphological opening
		erode(thresholdedImage, thresholdedImage, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		dilate(thresholdedImage, thresholdedImage, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		//morphological closing
		dilate(thresholdedImage, thresholdedImage, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		erode(thresholdedImage, thresholdedImage, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		//convert back to same type
		cvtColor(thresholdedImage, thresholdedImage, CV_GRAY2BGR);
		hconcat(mainImage, thresholdedImage, combinedView);
		//show windows
		imshow("Calibration View", combinedView);
		if (waitKey(20) == 27)
		{
			cont = 0;
		}
	}
	source.release();
	return 0;
}