#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include "CameraObject.h"
#include "fssimplewindow.h"
#include "3Dobjects.h"
#include <sstream>
#include <random>

#define NUM_RECT_PRISMS 250 // number of rectPrisms
#define NUM_TRI_PRISMS 250 // number of triPrisms
#define NUM_SPHERES 250 // number of Spheres

#define RIGID_BODY_SPACE 400
#define ROOT3 1.732

Objects::Objects() {
    
};

bool Objects::isOccupied(double location[3])
{
	return FALSE;
}

void Objects::createGrid() {
    glBegin(GL_LINES);
    int i;// Begin Creating Lines for Grid
    for (i = -10; i <= 10; i++) {                        // Loop the Grids as i
        glVertex3f(-10.0, 0.0, i);                    // Create Vertex for lower half
        glVertex3f(10.0, 0.0, i);                        // Create Vertex for lower half
        glVertex3f(i, 0.0, 10.0);                        // Create Vertex for lower half
        glVertex3f(i, 0.0, -10.0);                    // Create Vertex for lower half
        
        glVertex3f(-10.0, 5.0, i);                    // Create Vertex for higher half
        glVertex3f(10.0, 5.0, i);                        // Create Vertex for higher half
        glVertex3f(i, 5.0, 10.0);                        // Create Vertex for higher half
        glVertex3f(i, 5.0, -10.0);                    // Create Vertex for higher half
    }
    glEnd();
    
}


//Sphere class functions updated 11/29/18 by bobby

void Sphere::setParameters(double x0, double y0, double z0, double radius0, bool solid0) {
    x = x0;
    y = y0;
    z = z0;
    radius = radius0;
    solid = solid0;
}

void Sphere::setColor(double red, double green, double blue) {
    r = red;
    g = green;
    b = blue;
}

string Sphere::getInfo() {
    
    info = type + "\n" + to_string(x) + " " + to_string(y) + " " + to_string(z) + " " + to_string(r)
    + " " + to_string(g) + " " + to_string(b) + " " + to_string(radius) + " " + to_string(solid) + "\n";
    return info;
}

void Sphere::setInfo(string info) {
    const char *line; // temp variable to convert string to char
    line = info.c_str();
    istringstream ss(line);
    ss >> x >> y >> z >> r >> g >> b >> radius >> solid;
    
}

void Sphere::randomizeParameters(int i) {
    mt19937 generator (i);
    uniform_real_distribution<double> dis(5, 10);
    uniform_real_distribution<double> location(-1000.0, 1000.0);
    uniform_real_distribution<double> color(0, 255.9);
    
    r = color(generator);
    g = color(generator);
    b = color(generator);

    
    radius = dis(generator);
    x = location(generator);
    y = radius;
    z = location(generator);
    size = 100;
    solid = true;
}


void Sphere::draw(){
//    glShadeModel(GL_FLAT);
    int lats = 10;
    int longs = 10;
    int i, j;
	glColor3ub(r, g, b);
    for(i = 0; i <= lats; i++) {
        double lat0 = PI * (-0.5 + (double) (i - 1) / lats);
        double z0  = sin(lat0);
        double zr0 =  cos(lat0);
        
        double lat1 = PI * (-0.5 + (double) i / lats);
        double z1 = sin(lat1);
        double zr1 = cos(lat1);
        
        glBegin(GL_QUAD_STRIP);
        for(j = 0; j <= longs; j++) {
            double lng = 2 * PI * (double) (j - 1) / longs;
            double x1 = cos(lng);
            double y1 = sin(lng);
            
            glNormal3f(x + x1 * zr0 * radius, y + y1 * zr0 * radius, z + z0 * radius);
            glVertex3f(x + x1 * zr0 * radius, y + y1 * zr0 * radius, z + z0 * radius);
            glNormal3f(x + x1 * zr1 * radius, y + y1 * zr1 * radius, z + z1 * radius);
            glVertex3f(x + x1 * zr1 * radius, y + y1 * zr1 * radius, z + z1 * radius);
        }
        glEnd();
    }
} //Remade 11/30/18 by Will

// TriPrism Class added 11/30/18 by Will

string TriPrism::getInfo() {
    
    info = type + "\n" + to_string(x) + " " + to_string(y) + " " + to_string(z) + " " + to_string(base) +
    " " + to_string(length) +  " " + to_string(r) +
    " " + to_string(g) + " " + to_string(b) + "\n";
    return info;
}

void TriPrism::setInfo(string info) {
    const char *line; // temp variable to convert string to char
    line = info.c_str();
    istringstream ss(line);
    ss >> x >> y >> z >> base >> length >> r >> g >> b;
}

void TriPrism::randomizeBody(int i) {
    
    mt19937 generator (i);
    uniform_real_distribution<double> dis(5.0, 20.0);
    uniform_real_distribution<double> location(-1000.0, 1000.0);
    uniform_real_distribution<double> color(0, 255.9);

    base = dis(generator);
    length = dis(generator);
    
    r = color(generator);
    g = color(generator);
    b = color(generator);
  
    x = location(generator);
    y = length/2;
    z = location(generator);
   
}

void TriPrism::draw()
{
    glBegin(GL_TRIANGLES);
    glColor3ub(r,g,b);
    glVertex3d(x - base*ROOT3/6,y - length/2, z + base/2);
    glVertex3d(x - base*ROOT3/6,y - length/2, z - base/2);
    glVertex3d(x + base*ROOT3/3,y - length/2, z);
    
    glVertex3d(x - base*ROOT3/6,y + length/2, z + base/2);
    glVertex3d(x - base*ROOT3/6,y + length/2, z - base/2);
    glVertex3d(x + base*ROOT3/3,y + length/2, z);
    glEnd();

    
    glBegin(GL_QUADS);
    // 1st Rectangle (Green)
    glColor3ub(0, 255, 0);
    glVertex3d(x - base*ROOT3/6,y - length/2, z + base/2);
    glVertex3d(x - base*ROOT3/6,y - length/2, z - base/2);
    glVertex3d(x - base*ROOT3/6,y + length/2, z - base/2);
    glVertex3d(x - base*ROOT3/6,y + length/2, z + base/2);
    
    
    // 2nd Rectangle (Red)
    glColor3ub(255, 0, 0);
    glVertex3d(x - base*ROOT3/6,y - length/2, z - base/2);
    glVertex3d(x + base*ROOT3/3,y - length/2, z);
    glVertex3d(x + base*ROOT3/3,y + length/2, z);
    glVertex3d(x - base*ROOT3/6,y + length/2, z - base/2);
   
    // 3rd Rectangle (Blue)
    glColor3ub(0, 0, 255);
    glVertex3d(x + base*ROOT3/3,y - length/2, z);
    glVertex3d(x - base*ROOT3/6,y - length/2, z + base/2);
    glVertex3d(x - base*ROOT3/6,y + length/2, z + base/2);
    glVertex3d(x + base*ROOT3/3,y + length/2, z);

    glEnd();
} 

// RectPrism class added 11/27/18 by Will
string RectPrism::getInfo() {
    
    info = type + "\n" + to_string(x) + " " + to_string(y) + " " + to_string(z) + " " + to_string(width) +
    " " + to_string(length) + " " + to_string(height) + "\n";
    return info;
}

void RectPrism::setInfo(string info) {
    const char *line; // temp variable to convert string to char
    line = info.c_str();
    istringstream ss(line);
    ss >> x >> y >> z >> width >> length >> height;
    
}

void RectPrism::randomizeBody(int i) {

    mt19937 generator (i);
    uniform_real_distribution<double> dis(5.0, 20.0);
    uniform_real_distribution<double> location(-700, 700);

    width = dis(generator);
    height = dis(generator);
    length = dis(generator);
    
    
    x = location(generator);
    y = 0;
    z = location(generator);
    
}

void RectPrism::draw()
{
    
    glBegin(GL_QUADS);
    // Left face (Green)
    glColor3ub(0, 255, 0);
    glVertex3d(x - width / 2, y, z + height / 2);
    glVertex3d(x - width / 2, y + length, z + height / 2);
    glVertex3d(x + width / 2, y + length, z + height / 2);
    glVertex3d(x + width / 2, y , z + height / 2);
    
    // Right face (Black)
    glColor3ub(0, 0, 0);
    glVertex3d(x + width / 2, y, z - height / 2);
    glVertex3d(x + width / 2, y + length, z - height / 2);
    glVertex3d(x - width / 2, y + length, z - height / 2);
    glVertex3d(x - width / 2, y, z - height / 2);
    
    // Top face (Red)
    glColor3ub(255, 0, 0);
    glVertex3d(x + width / 2, y + length, z - height / 2);
    glVertex3d(x - width / 2, y + length, z - height / 2);
    glVertex3d(x - width / 2, y + length, z + height / 2);
    glVertex3d(x + width / 2, y + length, z + height / 2);
    
    // Bottom face (Yellow)
    glColor3ub(255, 255, 0);
    glVertex3d(x - width / 2, y, z - height / 2);
    glVertex3d(x + width / 2, y, z - height / 2);
    glVertex3d(x + width / 2, y, z + height / 2);
    glVertex3d(x - width / 2, y, z + height / 2);
    
    // Front face (Blue)
    glColor3ub(0, 0, 255);
    glVertex3d(x - width / 2, y + length, z - height / 2);
    glVertex3d(x - width / 2, y, z - height / 2);
    glVertex3d(x - width / 2, y, z + height / 2);
    glVertex3d(x - width / 2, y + length, z + height / 2);
    
    // Back face (Pink)
    glColor3ub(255, 0, 255);
    glVertex3d(x + width / 2, y + length, z - height / 2);
    glVertex3d(x + width / 2, y, z - height / 2);
    glVertex3d(x + width / 2, y, z + height / 2);
    glVertex3d(x + width / 2, y + length, z + height / 2);
    glEnd();
}

bool RectPrism::isOccupied(double location[3])
{
	if (location[0] >= x - width / 2 && location[0] <= x + width / 2)
	{
		if (location[1] >= y && location[1] <= y + length)
		{
			if (location[2] >= z-height/2 && location[2] <= z + height / 2)
			{
				return TRUE;
			}
		}
	}
	else
	{
		return FALSE;
	}
}

bool RectPrism::onTop(double location[3])
{
	if (location[0] >= x - width / 2 && location[0] <= x + width / 2)
	{
		if (location[1] >= y && location[1] <= y + length)
		{
			if (location[2] >= z - height / 2 && location[2] <= z + height / 2)
			{
				if (location[1] <= (y + length) + 5 && location[1] >= (y + length) - 1)
				{
					return TRUE;
				}
				
			}
		}
	}
	else
	{
		return FALSE;
	}
}




