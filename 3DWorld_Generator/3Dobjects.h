#pragma once

#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include "fssimplewindow.h"
#include <vector>

using namespace std;

class Objects {
public:


	int material;

	double x, y, z, size, typeNum;

	double info[5];

	bool solid = true;

	Objects();
	
	void createGrid();

	double center[3];

	virtual string getInfo() { return "Error!"; };

	virtual void setInfo(string info) { cout << "Error!"; };

	virtual void draw() { cout << "Error object not defined!"; };

	virtual bool isOccupied(double location[3]); //Virtual function to check for collision.

	virtual bool onTop(double location[3]) {
		return FALSE;
	}

};

class Sphere : public Objects {

public:
    string info;
    string type = "sphere";
    double x, y, z, r, g, b, radius, solid;
    void draw();
    string getInfo();
    void setInfo(string info);
    void setParameters(double x, double y, double z, double r, bool solid);// set parameters;
    void randomizeParameters(int i);
    void setColor(double r, double g, double b);
};

class TriPrism : public Objects {
public:
    string info;
    string type = "triangular prism";
    double base, length;
    int r, g, b;
    void setInfo(string info);
    string getInfo();

    void draw();
    void randomizeBody(int i);
};

class RectPrism : public Objects {
public:
    string info;
    string type = "rectangular prism";
    double x, y, z, width, height, length;

    void setInfo(string info);
    string getInfo();

	bool isOccupied(double location[3]);//pass an xyz to see if it occupies this space
	bool onTop(double location[3]);//used to detect collision specifically when standing on it. Pass it an xyz and it'll return if it is there or not
    void draw();
    void randomizeBody(int i); //used to create a body with random parameter

};
