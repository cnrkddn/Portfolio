#include <iostream>
#include <tuple>
#include <set>



using namespace std;

struct blueSquares {
	// set that stores coordinates of highlighted squares
	set<tuple<double, double>> coords;

};

class Grid {
protected:

	//Distance between squares
	double squareDist = 20;
	//Size of squares
	double squareSize = 15;
	//Number of squares in row and col (Given = 20x20 grid)
	int row = 20, col = 20;
	//Array which stores color of the squares
	tuple<double, double, double> colors[20][20];

	double initialX, initialY;

	int winLength, winWidth;

	int generateX, generateY;
	int generateSize = 100;
	bool generating = false;

	int resetX, resetY;
	int resetSize = 100;

public:

	Grid(int winLength, int winWidth);
	// draw grid
	void draw() const;
	// draw generate button
	void drawGenerate() const;
	// draw reset button
	void drawReset() const;
	
	void init();
	void highlightSquare(blueSquares &bs, int mouseX,int mouseY);
	// check whether the generate button has been clicked
	bool clickedGenerate(int mx, int my) {
		if (mx > generateX- generateSize/2 && mx< generateX + generateSize/2 &&
			my > generateY && my < generateY + generateSize/4) {
			generating = true;
			return true;
		}
		return false;
	}
	// check whether the reset button has been clicked
	bool clickedReset(int mx, int my) {
		if (mx > resetX - resetSize / 2 && mx< resetX + resetSize / 2 &&
			my > resetY && my < resetY + resetSize / 4) {
			generating = false;
			return true;
		}
		return false;
	}
};

class Circle {
protected:

	const double pi = 3.141592;
	const int circlePoints = 64;
	double initX = 500, initY = 450, initR = 300;
	double cx=0, cy=0, radius=0;

public:

	void initialCenterRadius(blueSquares bs);
	double rms(blueSquares bs, double x, double y, double r);
	void createCircle(blueSquares bs);
	void draw() const;
};