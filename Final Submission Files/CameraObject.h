#pragma once

#define PI 3.14159

// in charge of retaining camera location, orientation, and projection information

class CameraObject
{
public:
    double x, y, z;    // where you're located in terms of x, y, z
    double h, p, b;    // h = heading angle (left/right) , p = pitch angle (up/down), b = bank angle (rotaton about the z axis)
    
    double fov, nearZ, farZ;
    
    CameraObject();
    void Initialize(void);    // initializes camera to origin looking straight along z with 30 degree field of view and depth range 0.1 to 200
    void SetUpCameraProjection(void);
    void SetUpCameraTransformation(void);
    
    void GetForwardVector(double &vx, double &vy, double &vz);
    void printValues(char *result);
};


