#include "Part1.h"
#include "fssimplewindow.h"
#include <iostream>
#include <tuple>

int main()
{
	bool terminate = false;
	int winWidth = 800, winLength = 1000;
	int mouseEvent, lb, mb, rb, locX, locY;

	Grid grid(winLength,winWidth);
	BlueCircle blueCircle;
	RedCircle redCircle;

	FsOpenWindow(100, 100, winLength, winWidth, 1);

	while (!terminate) {

		FsPollDevice();

		switch (FsInkey()) {
		case FSKEY_ESC: terminate = true; // ESC ends program
			break;
		}

		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT); // make animation smooth

		grid.draw(); // draw 20x20 squares grid

		mouseEvent = FsGetMouseEvent(lb, mb, rb, locX, locY); // reads mouse action
		if (lb) { 
			grid.clear(); // clear all the highlighted sqaures whenever user reclick

			// center of blue and red circles is where the user first clicked
			blueCircle.setCenterCoord(make_tuple(locX,locY)); 
			redCircle.setCenterCoord(make_tuple(locX, locY));

			// user can drag the mouse as holding the left button to modify the radius
			while (lb) { 
				FsPollDevice();
				glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
				FsGetMouseEvent(lb, mb, rb, locX, locY);

				// update location of mouse cursor to update the radius
				blueCircle.updateMouseLoc(locX, locY); 
				blueCircle.calculateRadius(); 

				grid.draw();
				blueCircle.draw();

				FsSwapBuffers();
			}
		}
		// using blue circle's edge to determine which squares to highlight
		grid.highlightSquare(blueCircle); 

		redCircle.setBlueSquares(grid.getBlueSquares());
		redCircle.setSquareSize(grid.getSquareSize());
		// calculate radius of the red circles using vetices of the highlighted squares
		redCircle.calculateRadius();

		redCircle.draw();
		blueCircle.draw();


		FsSwapBuffers();
		FsSleep(25);
	}
}

