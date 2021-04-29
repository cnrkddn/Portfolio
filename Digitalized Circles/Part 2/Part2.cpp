
#include "Part2.h"
#include <iostream>
#include <tuple>
#include "fssimplewindow.h"
#include "ysglfontdata.h"

using namespace std;

Grid::Grid(int winLength, int winWidth) {
	// initialize the variables
	this->winLength = winLength;
	this->winWidth = winWidth;
	initialX = winLength / 2 - (row / 2 * (squareSize + squareDist)) + squareDist / 2;
	initialY = winWidth / 2 - (col / 2 * (squareSize + squareDist)) + squareDist / 2;
	generateX = winLength / 2;
	generateY = winLength*5/6;
	resetX = winLength *3/4;
	resetY = winLength * 5 / 6;
	init();
}

void Grid::init() {
	for (int i = 0;i < row;i++) {
		for (int j = 0;j < col;j++) {
			colors[i][j] = make_tuple(0.5, 0.5, 0.5);
		}
	}
}

void Grid::draw() const {

	double x = initialX;
	double y = initialY;

	for (int i = 0;i < row;i++) {
		x = initialX;
		for (int j = 0;j < col;j++) {
			auto color = colors[i][j];
			// get color of the each square
			glColor3f(get<0>(color), get<1>(color), get<2>(color));
			glBegin(GL_QUADS);

			glVertex2i(x, y);
			glVertex2i(x + squareSize, y);
			glVertex2i(x + squareSize, y + squareSize);
			glVertex2i(x, y + squareSize);

			x += (squareDist + squareSize);
		}
		y += (squareDist + squareSize);
	}
	glEnd();
	glFlush();
}

void Grid::drawGenerate() const {

	int x = generateX;
	int y = generateY;
	int size = generateSize;

	glColor3f(0.8,0.8,0.8);
	glBegin(GL_QUADS);

	glVertex2i(x-size/2, y);
	glVertex2i(x + size/2, y);
	glVertex2i(x +size/2, y + size/4);
	glVertex2i(x-size/2, y + size/4);

	glEnd();
	glFlush();

	if (generating == false) {
		glColor3f(0.0, 0.0, 0.0);
		glRasterPos2i(x - size/2+5, y + size /5 );
		YsGlDrawFontBitmap12x16("Generate");
	}
	else {
		glColor3f(0.0, 0.0, 0.0);
		glRasterPos2i(x - size/2+5, y + size / 5);
		YsGlDrawFontBitmap12x16("Reset");
	}

	glEnd();
	glFlush();
}

void Grid::drawReset() const {

	int x = resetX;
	int y = resetY;
	int size = resetSize;

	glColor3f(0.8, 0.8, 0.8);
	glBegin(GL_QUADS);

	glVertex2i(x - size / 2, y);
	glVertex2i(x + size / 2, y);
	glVertex2i(x + size / 2, y + size / 4);
	glVertex2i(x - size / 2, y + size / 4);

	glEnd();
	glFlush();

	if (generating == false) {
		glColor3f(0.0, 0.0, 0.0);
		glRasterPos2i(x - size / 2 + 5, y + size / 5);
		YsGlDrawFontBitmap12x16("Generate");
	}
	else {
		glColor3f(0.0, 0.0, 0.0);
		glRasterPos2i(x - size / 2 + 5, y + size / 5);
		YsGlDrawFontBitmap12x16("Reset");
	}

	glEnd();
	glFlush();
}

void Grid::highlightSquare(blueSquares &bs, int mx, int my) {

	double size = squareSize;
	double dist = squareDist;

	for (int i = 0;i < row;i++) {
		for (int j = 0;j < col;j++) {
			double sx = initialX + j * (size + dist);
			double sy = initialY + i * (size + dist);
			if (mx > sx && mx< sx + size &&
				my > sy && my < sy + size) {
				// center coordinate of the square
				sx = sx + squareSize / 2;
				sy = sy + squareSize / 2;
				// if clicked square's coordinate is not in the blue square set 
				// change the square color to blue and insert the coordinate in the blue square set
				if (bs.coords.find(make_tuple(sx, sy)) == bs.coords.end()) {
					colors[i][j] = make_tuple(0.0, 0.0, 1.0);
					bs.coords.insert(make_tuple(sx, sy));
				}
				// if clicked square's coordinate is already in the bs set
				// change the square color to gray and erase the coordinate
				else {
					colors[i][j] = make_tuple(0.5, 0.5, 0.5);
					bs.coords.erase(make_tuple(sx, sy));
				}
			}
		}
	}
}




void Circle::initialCenterRadius(blueSquares bs) {
	double xx, xy, x, yy, y, n, zz, xz, yz, z;
	double avgX, avgY;
	double det = 0, localX = 0, localY = 0;
	xx = xy = x = yy = y = n = xz = yz = zz = z = 0;

	// calculate the average
	for (auto it = bs.coords.begin();it != bs.coords.end();++it) {
		double xi = get<0>(*it);
		double yi = get<1>(*it);
		x += xi;
		y += yi;
		n++;
	}

	avgX = x / n; // mean x
	avgY = y / n; // mean y

	for (auto it = bs.coords.begin();it != bs.coords.end();++it) {
		double xi = get<0>(*it) - avgX;
		double yi = get<1>(*it) - avgY;
		double zi = (xi*xi + yi * yi);
		yy += yi * yi;
		xx += xi * xi;
		xy += xi * yi;
		xz += xi * zi;
		yz += yi * zi;
		zz += zi * zi;
	}
	// calculate for the average value

	xx = xx / n;
	yy = yy / n;
	xy = xy / n;
	xz = xz / n;
	yz = yz / n;
	zz = zz / n;
	z = xx + yy;

	det = xx * yy - xy * xy + z;
	localX = (xz*yy - yz * xy) / (2 * det);
	localY = (yz*xx - xz * xy) / (2 * det);
	initX = localX + (x / n);
	initY = localY + (y / n);
	initR = sqrt(localX*localX + localY * localY + z);
}

double Circle::rms(blueSquares bs, double x, double y, double r) {
	
	double sum = 0, n=0, dx, dy;

	for (auto it = bs.coords.begin();it != bs.coords.end();++it) {
		double dx = get<0>(*it)-x;
		double dy = get<1>(*it)-y;
		sum += (sqrt(dx*dx + dy * dy) - r)*(sqrt(dx*dx + dy * dy) - r);
		n++;
	}
	return sqrt(sum / n);
}

void Circle::createCircle(blueSquares bs) {
	
	//Levenberg-Marquardt Circle Fit

	// Enable below fuction to optimize the initial value
	//initialCenterRadius(bs);

	double lambda = 1;
	double eps = 1.0e-10;
	double iterMax = 90, coordMax=1e6;
	double lambdaSqrt = sqrt(lambda);
	double oldX, oldY, oldR, old_g, old_rms;
	double newX=initX, newY=initY, newR=initR,new_g,new_rms;
	double sum_u, sum_v, sum_uu, sum_vv, sum_uv, sum_r;
	double sum_x, sum_y, n, meanX, meanY;
	double innerIter = 0;

	sum_u= sum_v= sum_uu= sum_vv= sum_uv= sum_r=sum_x= sum_y= n=0;
	new_rms = rms(bs, newX, newY, newR);

	// solve for the mean of x and y for centroid
	for (auto it = bs.coords.begin();it != bs.coords.end();++it) {
		double xi = get<0>(*it);
		double yi = get<1>(*it);
		sum_x += xi;
		sum_y += yi;
		n++;
	}

	meanX = sum_x / n;
	meanY = sum_y / n;

	double g11, g12, g13, g22, g23, g33;
	double D1, D2, D3;
	double dX, dY, dR;

	for (int i = 0;i < iterMax;i++) {
		oldX = newX; oldY = newY; oldR = newR;old_rms = new_rms;
		for (auto it = bs.coords.begin();it != bs.coords.end();++it) {
			// Centering the data to reduce round-off errors
			double dx = get<0>(*it) - oldX;
			double dy = get<1>(*it) - oldY;
			double ri = sqrt(dx*dx + dy * dy);
			// Scale the data to amek values of order one
			// u and v are sample means
			double u = dx / ri;
			double v = dy / ri;
			// pre-calculate the necessary variables for the ease of use
			sum_u += u;
			sum_v += v;
			sum_uu += u * u;
			sum_vv += v * v;
			sum_uv += u * v;
			sum_r += ri;
		}

		sum_u /= n;	sum_v /= n; sum_r /= n;
		sum_uu /= n; sum_vv /= n; sum_uv /= n;
		
		// F =  Objective Function
		// F1,F2,F3 are the gradient of F
		double F1 = oldX + oldR * sum_u-meanX;
		double F2 = oldY + oldR* sum_v-meanY;
		double F3 = oldR - sum_r;

		// g = transpose(Q)*gradient(F)
		old_g = new_g = sqrt(F1*F1 + F2 * F2 + F3 * F3);

		innerIter = 0;

		// Full Newton Minimization
		while (true) {
			
			// solve for D and g matrix for eigenvalue decompostiion
			// g orthogonal matrix
			g11 = sqrt(sum_uu+lambda);
			g12 = sum_uv / g11;
			g13 = sum_u / g11;
			g22 = sqrt(sum_vv+lambda - g12 * g12);
			g23 = (sum_v - g12 * g13) / g22;
			g33 = sqrt(lambda + 1 - g13 * g13 - g23 * g23);

			// D diagonal matrix
			D1 = F1 / g11;
			D2 = (F2 - g12 * D1) / g22;
			D3 = (F3 - g13 * D1 - g23 * D2) / g33;

			// eigenvalue decomposition
			dR = D3 / g33;
			dY = (D2 - g23 * dR) / g22;
			dX = (D1 - g12 * dY - g13 * dR) / g11;

			if ((abs(dR) + abs(dX) + abs(dY)) / (oldR+1) < eps) {
				cx = oldX; cy = oldY; radius = oldR;
				return;
			}

			newX = oldX - dX;
			newY = oldY - dY;
			newR = oldR - dR;
			
			if (abs(newX) > coordMax || abs(newY) > coordMax) { 
				cx = oldX; cy = oldY; radius = oldR;
				return;
			}

			if (newR <= 0.)
			{
				lambda *= 10;
				if (++innerIter > iterMax) {
					cx = oldX; cy = oldY; radius = oldR;
					return;
				}
				continue;
			}

			new_rms = rms(bs, newX, newY, newR);
			if (new_rms < old_rms)  
			{
				lambda /= 2;
				break;
			}
			else                    
			{
				if (++innerIter > iterMax) {
					cx = oldX; cy = oldY; radius = oldR;
					return;
				}
				lambda *= 10;
				continue;
			}
		}
	}
	cx = oldX; cy = oldY; radius = oldR;
}

void Circle::draw() const {

	glColor3f(0.0,0.0,1.0);
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