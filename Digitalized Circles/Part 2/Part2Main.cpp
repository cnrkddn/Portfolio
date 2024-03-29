#include "Part2.h"
#include "fssimplewindow.h"
#include <iostream>
#include <tuple>

int main()
{
	bool terminate = false, generating = false;
	int winLength = 1000;
	int winWidth = 900;
	int mouseEvent, lb, mb, rb, locX, locY;
	
	Grid grid(winLength, winWidth);
	Circle circle;
	blueSquares bs;

	FsOpenWindow(100, 50, winLength, winWidth, 1);

	while (!terminate) {

		FsPollDevice();

		switch (FsInkey()) {
		case FSKEY_ESC: terminate = true; // ESC ends program
			break;
		}

		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);

		grid.draw();
		// draw generate button only when the user not yet generated the points
		if (generating == false) {
			grid.drawGenerate();
		}
		else {
			// draw reset button only when the points generated
			grid.drawReset();
		}
		
		mouseEvent = FsGetMouseEvent(lb, mb, rb, locX, locY);
		if (lb) {
			// when the left button is clicked
			// check if the user clicked generate button or reset button
			grid.highlightSquare(bs, locX, locY);
			if (grid.clickedGenerate(locX, locY)&&generating==false) {
				generating = true;
			}
			if(grid.clickedReset(locX,locY)&&generating==true){
				bs.coords.clear();
				grid.init();
				generating = false;
			}
		}

		// if the user clicked generate, draw the circle
		if (generating == true) {
			circle.createCircle(bs);
			circle.draw();
		}

		FsSwapBuffers();
		FsSleep(100);
	}
}
