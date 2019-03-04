
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <iostream>
#include <vector>

using namespace std;
using namespace cv;
int main()
{
	int index = 0;
	//index will be amount of cameras possible
	vector<VideoCapture> sources (15);
	vector<Mat> cams (15);
	//vector capped at 15 to store cameras
	int cont = 1; //for the second while loop, check to see if still display
	for (int i = 0; i < 15; i++)
	{
		VideoCapture source(index);
		if (!source.isOpened())
		{
			break;
		}
		index++;
	}
	// ABOVE CODE SCANS AND TRIES TO SEE HOW MANY CAMERAS ON DEVICES
	//now display frames for each camera
	for (int i = 0; i < index; i++)
	{
		VideoCapture source(index);
		sources[i] = source;
	}
	while (cont)
	{
		//display image now with labeled indexes
		for (int i = 0; i < index; i++)
		{
			Mat temp;
			sources[i].read(temp);
			cout << temp;
			if (!cams[i].empty())
			{
				imshow(to_string(i), cams[i]);
				if (waitKey(35) == 27) //check if ESC key pressed
				{
					cont = false;
				}
			}
		}
	}
	//remember to release cameras afterwards
	
}