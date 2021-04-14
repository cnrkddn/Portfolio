#pragma once
#include <vector>
#include "3Dobjects.h"

using namespace std;

class Container { // Container class has vector called Container that will contain all the shapes.
public:
    
    int numShape; // Number of shapes in the vector.
    vector<Objects*> container; //It contains all the shapes.
    
public:
    void store(Objects* shape); // This function stores all the shapes in container
    void save(const string fName); // save shapes in text file
    void load(const string fName); // load shapes
	void create(const string shapeName);
    void draw();
	bool isOccupied(double location[3]);
	bool onTop(double location[3]);
};

