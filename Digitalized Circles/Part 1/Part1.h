#include <tuple>
#include <iostream>
#include <queue>
#include <deque>

using namespace std;

class Circle {
// Parent circle class to share common variables and methods
protected:

	const double pi = 3.141592;
	const int circlePoints=64;
	double cx, cy; // center of both blue and red circles

public:
	
	void setCenterCoord(tuple<int,int> coord) {
		cx = get<0>(coord);
		cy = get<1>(coord);
	}
	tuple<double, double> getCenterCoord() {
		return make_tuple(cx, cy);
	}
	// both methods are required for child classes
	virtual void calculateRadius() = 0;
	virtual void draw() const=0;
};


class BlueCircle : public Circle {
	// inherits character from circle class
private:

	tuple<double, double, double> edgeColor=make_tuple(0.0,0.0,1.0); // blue
	double radius,mouseX,mouseY;

public:
	double getRadius(){
		return radius;
	}
	void updateMouseLoc(double locX, double locY) {
		mouseX = locX;
		mouseY = locY;
	}
	void calculateRadius() {
		double x = mouseX - cx;
		double y = mouseY - cy;
		radius = sqrt(x * x + y * y);
	} //modify parent's method
	void draw() const;
};

class RedCircle :public Circle {
	// inherits character from circle class
private:
	tuple<double, double, double> edgeColor = make_tuple(1.0, 0.0, 0.0);
	// there are always two red circles, thus two radius
	double outerRadius,innerRadius,squareSize;
	queue<tuple<double, double>> blueSquares;

public:
	void setBlueSquares(queue<tuple<double, double>> blueSquares) {
		if (blueSquares.size() > 0) {
			this->blueSquares = blueSquares;
			double x = cx - get<0>(blueSquares.front());
			double y = cy - get<1>(blueSquares.front());
			double initialRadius = sqrt(x * x + y * y);
			outerRadius = initialRadius;
			innerRadius = initialRadius;
		}
	}
	void setSquareSize(double squareSize) {
		this->squareSize = squareSize;
	}
	// check distance between the highlighted square and center point to find furthest and nearest ones
	void checkDistance(double x,double y);
	void calculateRadius(); // calculate for both radius
	void draw() const;

};

class Grid {
protected:

	//Distance between squares
	double squareDist = 20;
	//Size of squares
	double squareSize = 10;
	//Number of squares in row and col (Given = 20x20 grid)
	int row = 20, col = 20;
	//Array which stores color of the squares
	tuple<double, double, double> colors[20][20];

	double initialX, initialY;
	int winLength, winWidth;

	//store top-left corner coordinates of all the highlighted(blue) squares
	queue<tuple<double,double>> blueSquares;

public:

	Grid(int winLength, int winWidth);
	void clear();
	void draw() const;
	queue<tuple<double, double>> getBlueSquares() {
		return blueSquares;
	}
	double getSquareSize() {
		return squareSize;
	}
	// find all the squares that are close to the blue circle's edge
	bool checkCollision(BlueCircle circle, int row, int col);
	void highlightSquare(BlueCircle circle);
};

