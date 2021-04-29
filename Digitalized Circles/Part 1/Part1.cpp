#include <iostream>
#include <tuple>
#include "fssimplewindow.h"
#include "Part1.h"

using namespace std;

Grid::Grid(int winLength,int winWidth) {
	// initialize all the grid variables
	this->winLength = winLength;
	this->winWidth = winWidth;
	// initailize x and y coordinate of the first grid square
	initialX = winLength / 2 - (row / 2 * (squareSize + squareDist)) + squareDist / 2;
	initialY = winWidth / 2 - (col / 2 * (squareSize + squareDist)) + squareDist / 2;
	// initialize all the squares as gray
	for (int i = 0;i < row;i++) {
		for (int j = 0;j < col;j++) {
			colors[i][j] = make_tuple(0.5, 0.5, 0.5);
		}
	}
}

void Grid::clear() {
	
	// remove all the highlighted squares from the grid
	for (int i = 0;i < row;i++) {
		for (int j = 0;j < col;j++) {
			colors[i][j] = make_tuple(0.5, 0.5, 0.5);
		}
	}
	// empty queue that contains coordinate information of bluesquares
	queue<tuple<double, double>> empty;
	swap(blueSquares,empty);
	
}

void Grid::draw() const{

	double x = initialX;
	double y = initialY;

	// draw 20X20 squares, all equally distanced
	for (int i = 0;i < row;i++) {
		x = initialX;
		for (int j = 0;j < col;j++) {
			auto color = colors[i][j];
			glColor3f(get<0>(color), get<1>(color), get<2>(color));
			glBegin(GL_QUADS);

			glVertex2i(x, y);
			glVertex2i(x + squareSize, y);
			glVertex2i(x + squareSize, y+squareSize);
			glVertex2i(x, y + squareSize);

			x += (squareDist + squareSize);
		}
		y += (squareDist + squareSize);
	}
	glEnd();
	glFlush();
}



bool Grid::checkCollision(BlueCircle circle, int i, int j) {
	double cx = get<0>(circle.getCenterCoord());
	double cy = get<1>(circle.getCenterCoord());
	double radius = circle.getRadius();

	double size = squareSize;
	double dist = squareDist;

	double sx = initialX + j*(size+dist);
	double sy = initialY + i * (size + dist);
	// loop thru all the points on the edge of the blue circle
	for (int i = 0;i < 360;i += 5) {
		double x = cx + cos(i)*radius;
		double y = cy + sin(i)*radius;
		int th=1;
		// if the edge point collide with the square territory, make that square blue(highlight)
		if (x > sx - dist / 2 +th&& x<sx + size + dist / 2-th&&
			y>sy - dist / 2 + th && y < sy + size + dist / 2-th){ // territory is bigger than actual square
			blueSquares.push(make_tuple(sx, sy));
			return true;
		}
	}
	return false;
}

void Grid::highlightSquare(BlueCircle circle) {
	for (int i = 0;i < row;i++) {
		for (int j = 0;j < col;j++) {
			if (checkCollision(circle, i, j)) {
				colors[i][j] = make_tuple(0.0, 0.0, 1.0);
			}
		}
	}
}


void BlueCircle::draw() const {

	glColor3f(get<0>(edgeColor), get<1>(edgeColor), get<2>(edgeColor));
	glLineWidth(3);
	glBegin(GL_LINE_LOOP);
	for (int i = 0;i < circlePoints;i++) {
		double angle = (double)i * 2 * pi / circlePoints;
		double x = (double)cx + cos(angle)*(double)radius;
		double y = (double)cy + sin(angle)*(double)radius;
		glVertex2d(x, y);
	}
	glEnd();
	glFlush();
}

void RedCircle::checkDistance(double x, double y) {
	double dist = sqrt(x * x + y * y);
	// if the distance between square and the center point is biggest
	// set that point as the outer radius
	if (dist > outerRadius) {
		outerRadius = dist;
	}
	// else if it is the smallest set that as the inner radius
	else if (dist < innerRadius) {
		innerRadius = dist;
	}
}
void RedCircle::calculateRadius() {
	while (!blueSquares.empty()) {
		double sx = get<0>(blueSquares.front());
		double sy = get<1>(blueSquares.front());

		// square has four corners
		// check all the corners to check whether the square is either furthest or nearest
		checkDistance(sx-cx, sy-cy); // left-top
		checkDistance(sx+squareSize-cx, sy-cy); // right-top
		checkDistance(sx + squareSize-cx, sy + squareSize-cy); //right-bottom
		checkDistance(sx-cx, sy + squareSize-cy); // left-bottom
		blueSquares.pop();
	}
}

void RedCircle::draw() const {

	glColor3f(get<0>(edgeColor), get<1>(edgeColor), get<2>(edgeColor));
	glLineWidth(3);
	// draw outer red circle
	glBegin(GL_LINE_LOOP);
	for (int i = 0;i < circlePoints;i++) {
		double angle = (double)i * 2 * pi / circlePoints;
		double x = (double)cx + cos(angle)*(double)outerRadius;
		double y = (double)cy + sin(angle)*(double)outerRadius;
		glVertex2d(x, y);
	}
	glEnd();
	glFlush();
	// draw inner red circle
	glColor3f(get<0>(edgeColor), get<1>(edgeColor), get<2>(edgeColor));
	glLineWidth(3);
	glBegin(GL_LINE_LOOP);
	for (int i = 0;i < circlePoints;i++) {
		double angle = (double)i * 2 * pi / circlePoints;
		double x = (double)cx + cos(angle)*(double)innerRadius;
		double y = (double)cy + sin(angle)*(double)innerRadius;
		glVertex2d(x, y);
	}
	glEnd();
	glFlush();
}