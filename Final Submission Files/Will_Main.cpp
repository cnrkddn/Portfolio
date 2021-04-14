
#include <stdio.h>
#include <iostream>
#include <math.h>
#include "fssimplewindow.h"
#include "CameraObject.h"
#include "3Dobjects.h"
#include <string>
#include "fssimplewindow.h"
#include "ysglfontdata.h"
#include "SaveLoad.h"
#include <time.h>


using namespace std;

#define NUM_RECT_PRISMS 250 // number of rectPrisms
#define NUM_TRI_PRISMS 250 // number of triPrisms
#define NUM_SPHERES 250 // number of Spheres
#define RIGID_BODY_SPACE 400 // because, why not?
#define PI 3.141592653589793


// create container object


int main()
{
    //+++++++++++++++++++++++++++++++++++++
    
    // edit for rigid bodies
    // basically goes through each generated body, and initializes with position, velocity, acceleration
    srand(time(NULL));
    
    Container bodies;
    
    RectPrism* tempRect = new RectPrism;
    
    for (int i = 0; i < NUM_RECT_PRISMS; i++)
    {
        tempRect = new RectPrism;
        tempRect->randomizeBody(rand());
        bodies.store(tempRect);
        
//        cout << temp << " ";
//        cout << temp->center[0] << endl;
    }
    
    TriPrism* tempTri = new TriPrism;
    for (int i = 0; i < NUM_TRI_PRISMS; i++)
    {
        tempTri = new TriPrism;
        tempTri->randomizeBody(rand());
        bodies.store(tempTri);
        
        //        cout << temp << " ";
        //        cout << temp->center[0] << endl;
    }
    
    Sphere* tempSphere = new Sphere;
    
    for (int i = 0; i < NUM_SPHERES; i++)
    {
        tempSphere = new Sphere;
        tempSphere->randomizeParameters(rand());
        bodies.store(tempSphere);
        
        cout << tempSphere->x << endl;

    }
    //+++++++++++++++++++++++++++++++++++++
    
    // more camera/flythrough main
    
    bool terminate = false;
    CameraObject camera;
    int x, gridSpacing = 20;
    double gridSize = 1000;
    int wid, hei;
    char data[255];
    
    camera.z = 10.0;
    camera.y = 5.0;
    camera.farZ = 1000.;
    FsOpenWindow(16, 16, 800, 600, 1);
    
    while (!terminate)
    {
        FsPollDevice();
        
        FsGetWindowSize(wid, hei);
        
        int key = FsInkey();
        switch (key)
        {
            case FSKEY_ESC:
                terminate = true;
                break;
        }
        if (0 != FsGetKeyState(FSKEY_LEFT))
            camera.h += PI / 180.0;
        
        if (0 != FsGetKeyState(FSKEY_RIGHT))
            camera.h -= PI / 180.0;
        
        if (0 != FsGetKeyState(FSKEY_UP))
            camera.p += PI / 180.0;
        
        if (0 != FsGetKeyState(FSKEY_DOWN))
            camera.p -= PI / 180.0;
        
        if (0 != FsGetKeyState(FSKEY_W)) {
            double vx, vy, vz;
            camera.GetForwardVector(vx, vy, vz);
			double destination[3] = { camera.x + vx * 1 , camera.y + vy * 1 , camera.z + vz * 1 };
			if (bodies.isOccupied(destination) == FALSE)
			{
				camera.x += vx * 1;
				camera.y += vy * 1;
				camera.z += vz * 1;
			}
			else
			{
				//cout << "Collision\n"; // was an indicator for collision
			}
            
        }
        if (0 != FsGetKeyState(FSKEY_S)) {
			double vx, vy, vz;
			camera.GetForwardVector(vx, vy, vz);
			double destination[3] = { camera.x - vx * 1 , camera.y - vy * 1 , camera.z - vz * 1 };
			if (bodies.isOccupied(destination) == FALSE)
			{
				camera.x -= vx * 1;
				camera.y -= vy * 1;
				camera.z -= vz * 1;
			}
			
        }
		if (0 != FsGetKeyState(FSKEY_C))
		{
			string temp;
			cout << "What object would you like to create?";
			getline(cin, temp);
			bodies.create(temp);
		}


        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
        
        glViewport(0, 0, wid, hei);
        
        // Set up 3D drawing
        camera.SetUpCameraProjection();
        camera.SetUpCameraTransformation();
        
        glEnable(GL_DEPTH_TEST);            // enables depth buffer
        glEnable(GL_POLYGON_OFFSET_FILL);
        glPolygonOffset(1, 1);
        // 3D drawing from here
        
        //+++++++++++++++++++++++++++++++++++++
        
        glPushMatrix(); // allows for rotation of bodies around defined axes
        bodies.draw();
        glPopMatrix(); // stops rotation so that you dont rotate the entire grid
        //+++++++++++++++++++++++++++++++++++++
//        glEnable(GL_LIGHTING);              // Set up ambient light.
//        GLfloat ambient_intensity[] = { 0.3, 0.3, 0.3, 1.0 };
//        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_intensity);
        
        glBegin(GL_LINES);
        for (x = -gridSize; x <= gridSize; x += gridSpacing)
        {
            glColor3ub(0, 0, x % 256);
            glVertex3i(x, 0, -gridSize);
            glVertex3i(x, 0, gridSize);
            glVertex3i(-gridSize, 0, x);
            glVertex3i(gridSize, 0, x);
        }
        glEnd();
        
        // Set up 2D drawing
        glMatrixMode(GL_PROJECTION);    // tells OpenGL that the program is about to set a projection matrix
        glLoadIdentity();                // resets the projection matrix
        glOrtho(0, (float)wid - 1, (float)hei - 1, 0, -1, 1);
        
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        
        glDisable(GL_DEPTH_TEST);
        
        // **2D drawing must be done here**
        
        camera.printValues(data);
        //std::cout << data << std::endl;
        glColor3ub(0, 0, 0);
        glRasterPos2i(10, 15);
        
        
        //+++++++++++++++++++++++++++++++++++++
        // updates the objects
//        for (int i = 0; i < NUM_RIGID_BODIES; i++)
//        {
//            body[i].runSimulation();
//        }
        //+++++++++++++++++++++++++++++++++++++
        
        
        YsGlDrawFontBitmap6x10(data);
        
        FsSwapBuffers();
        FsSleep(10);
    }
    
    bodies.save("fileName"); 
    return 0;
}


