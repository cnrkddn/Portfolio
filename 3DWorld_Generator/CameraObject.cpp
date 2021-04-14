#include <stdio.h>
#include <string>
#include <math.h>
#include "fssimplewindow.h"
#include "ysglfontdata.h"
#include "SaveLoad.h"
#include "3Dobjects.h"
#include "CameraObject.h"

CameraObject::CameraObject()
{
    Initialize();
}

void CameraObject::Initialize(void)
{
    x = 0;
    y = 0;
    z = 0;
    h = 0;
    p = 0;
    b = 0;
    
    fov = PI / 6.0;  // 30 degree
    nearZ = 0.1;
    farZ = 200.0;
}

void CameraObject::SetUpCameraProjection(void)
{
    int wid, hei;
    double aspect;
    
    FsGetWindowSize(wid, hei);
    aspect = (double)wid / (double)hei;
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(fov*180.0 / PI, aspect, nearZ, farZ);
}

void CameraObject::SetUpCameraTransformation(void)
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glRotated(-b * 180.0 / PI, 0.0, 0.0, 1.0);    // (angle of rotation in degrees) , (axis of rotation)
    glRotated(-p * 180.0 / PI, 1.0, 0.0, 0.0);
    glRotated(-h * 180.0 / PI, 0.0, 1.0, 0.0);
    glTranslated(-x, -y, -z);
}

void CameraObject::GetForwardVector(double &vx, double &vy, double &vz)
{
    vx = -cos(p)*sin(h);
    vy = sin(p);
    vz = -cos(p)*cos(h);
}

void CameraObject::printValues(char *result)
{
    using namespace std;
    string temp;
    temp = " x=" + to_string(x);
    temp += " y=" + to_string(y);
    temp += " z=" + to_string(z);
    temp += " h=" + to_string(h);
    temp += " p=" + to_string(p);
    temp += " b=" + to_string(b);
    strcpy(result, temp.c_str());
}

