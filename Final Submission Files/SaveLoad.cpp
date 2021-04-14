
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "3Dobjects.h"
#include "SaveLoad.h"

using namespace std;

void Container::store(Objects* shape) {
    container.push_back(shape);
}

void Container::save(const string fName) {
    
    numShape = (int)container.size();
    // save current pixels
    ofstream outfile(fName);
    if (outfile.is_open())
    {
        outfile << to_string(numShape) << "\n";
        
        for (int i = 0; i < numShape; i++) {
            outfile << container[i]->getInfo();
        }
        outfile.close();
    }
    else cout << "Unable to open file";
}

void Container::load(const string fName) {
    
    container.clear();
    ifstream inFile;
    inFile.open(fName);
    string str; //temp variable to store line from file
    
    
    Objects* temp = new Objects;
    
    if (inFile.is_open()) {
        
        inFile >> numShape;
        getline(inFile, str);
        
        for (int i = 0; i < numShape; i++) {
            if (!inFile.eof()) {  // just in case
                
                getline(inFile, str);
                
               
                if (str == "sphere") {
                    temp = new Sphere;
                }
                else if (str == "rectangular prism"){
                    temp =  new RectPrism;
                }
               
                getline(inFile, str);
                temp->setInfo(str);
                container.push_back(temp);// Add temp at the back
            }
        }
        inFile.close();
    }
    else {
        cout << "\nUnable to open file";
    }
}

void Container::draw() {
    // it calls draw function of all shapes
    for (int i = 0; i < (int)container.size(); i++) {
        container[i]->draw();
    }
    
}

void Container::create(const string shapeName) {
	string fill;
	
	if (shapeName == "sphere") {
		Sphere* temp = new Sphere;
		cout << "Choose location(x,y,z):(separate by space, no range, ex:10 10 10)\n";
		cin >> temp->x >> temp->y >> temp->z;
		cout << "Choose color:(r,g,b)(separate by space, 0 <= range <= 255, ex:255 255 255)\n";
		cin >> temp->r >> temp->g >> temp->b;
		cout << "Choose radius:(one integer, no range, ex:15)\n";
		cin >> temp->radius;
		cout << "Do you want to fill the shape?(yes or no, ex:yes)\n";
		cin >> fill;
		if (fill == "yes") {
			temp->solid = true;
		}
		else {
			temp->solid = false;
		}
		container.push_back(temp);
	}

	else if (shapeName == "rectangular prism") {
		RectPrism* temp = new RectPrism;
		cout << "Choose location(x,y,z):(separate by space, no range, ex:10 10 10)\n";
		cin >> temp->x >> temp->y >> temp->z;
		//cout << "Choose color:(r,g,b)(separate by space, 0 <= range <= 255, ex:255 255 255)\n"; //RGB not enabled for this class
		//cin >> temp->r >> temp->g >> temp->b;
		cout << "Choose size(width,height,length):(separate by space, no range, ex:20 20 20)\n";
		cin >> temp->width >> temp->length >> temp->height;
		//cout << "Do you want to fill the shape?(yes or no, ex:yes)\n"; //fill not a parameter in this class
		//cin >> fill;
		//if (fill == "yes") {
		//	temp->solid = true;
		//}
		//else {
		//	temp->solid = false;
		//}
		container.push_back(temp);
	}
	else if (shapeName == "triangular prism") {
		TriPrism* temp = new TriPrism;
		cout << "Choose location(x,y,z):(separate by space, no range, ex:10 10 10)\n";
		cin >> temp->x >> temp->y >> temp->z;
		cout << "Choose size(base,length):(separate by space, no range, ex:20 20)\n";
		cin >> temp->base >> temp->length;
		
		container.push_back(temp);
	}
	else
	{
		cout << "invalid entry " << shapeName << endl;
	}
	cout << "Done creating" << endl;
}

bool Container::isOccupied(double location[3]) {
	// it calls draw function of all shapes
	for (int i = 0; i < (int)container.size(); i++) {
		if (container[i]->isOccupied(location) == TRUE)
		{
			return TRUE;
		}
	}
	return FALSE;
}

bool Container::onTop(double location[3]) {
	// it calls draw function of all shapes
	for (int i = 0; i < (int)container.size(); i++) {
		if (container[i]->onTop(location) == TRUE)
		{
			return TRUE;
		}
	}
	return FALSE;
}



