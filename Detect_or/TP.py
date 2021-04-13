### Kangwoo Choo 15-112 Term Project

from tkinter import *
from PIL import Image,ImageTk
import random
import numpy as np
import cv2
import sys
import time
import math
import collections
import coloredlogs, logging
sys.setrecursionlimit(10000)
####################################
# customize these functions
####################################

def init(data):
    
    data.helpX, data.helpY = data.width*1/13, data.height*1/13
    data.carWidth,data.carHeight = 25,50
    data.cursorX, data.cursorY = 0,0
    data.helpFont,data.helpColor = None,"white"
    data.redCarSize,data.blueCarSize,data.yellowCarSize = 0,0,0
    data.redCarX,data.redCarY = data.width*2/4, data.height*3/4
    data.blueCarX, data.blueCarY = data.width*1/4, data.height*3/4
    data.yellowCarX, data.yellowCarY = data.width*3/4, data.height*3/4
    data.backX,data.backY  = data.width*1/13,data.height*1/13
    data.backFont,data.nameFont = None, None
    data.nameColor,data.lineColor = None, "beige"
    data.blueCar = Image.open("blueCar.png")
    data.yellowCar = Image.open("yellowCar.png")
    data.redCar = Image.open("redCar.png")
    data.isSelectedCar = None
    data.position = 0
    data.carX, data.carY = data.width/2, data.height*7/8
    data.level = 1
    initHelper(data)
    intiIs(data)
    
def initHelper(data):
    data.numOne, data.treeOneY = None, 0
    data.numTwo, data.treeTwoY = None, 0
    data.numThree, data.treeThreeY = None, 0
    data.numFour, data.treeFourY = None, 0
    data.obstacles,data.numObs = [], 2
    data.obsX,data.obsType = 0,None
    data.carPoints = []
    data.roadLeft,data.roadRight = data.width/5, data.width*4/5
    data.items,data.numItems = [],0
    data.itemType = None
    data.time = 0
    data.score = 0
    data.health,data.maxHealth = 6,6
    data.special, data.maxSpecial = 2,3
    data.carSize = (100,130)
    data.speedSaved,data.objectSpeedSaved  = 10,10
    data.latestObs = None
    data.freqItem = 150
    data.tutorialText =   "Hold RED on Right hand, show only red to move right"

def intiIs(data):
    data.isGameStart = False
    data.isHelp = False
    data.useMotion = True
    data.isReady = False
    data.isMenu = False
    data.isGameOver = False
    data.isSpecial = False
    data.isShield = False
    data.isMoving = False
    
def mouseMotion(event, data):
    data.cursorX, data.cursorY = event.x, event.y

def mousePressed(event, data):
    carHeight, carWidth = 30,10
    if(event.x > data.helpX-carHeight and event.x < data.helpX+carHeight and
        event.y > data.helpY-carWidth and event.y < data.helpY+carWidth*2 and 
        data.isHelp == False):
        data.isHelp = True
    elif(event.x > data.backX-carHeight and event.x < data.backX+carHeight and
        event.y > data.backY-carWidth and event.y < data.backY+carWidth*2 and 
        data.isHelp == True):
        data.isHelp = False
    else:
        mousePressedCars(event, data)
    
def mousePressedCars(event, data):
    if(event.x > data.redCarX-30 and event.x < data.redCarX+30 and
        event.y > data.redCarY-60 and event.y < data.redCarY+60):
        cursorPositionStartRedCar(data)
        data.isSelectedCar = Image.open("redCar.png")
        data.isGameStart = True
    elif(event.x > data.blueCarX-30 and event.x < data.blueCarX+30 and
        event.y > data.blueCarY-60 and event.y < data.blueCarY+60):
        data.blueCarSize = (130,160)
        data.nameColor,data.lineColor = "darkturquoise","darkturquoise"
        data.nameFont = "Helvetica 52 bold"
        data.redCar, data.yellowCar = None, None
        data.isSelectedCar = Image.open("blueCar.png")
        data.isGameStart = True
    elif(event.x>data.yellowCarX-30 and event.x<data.yellowCarX+30 and
        event.y >data.yellowCarY-60 and event.y < data.yellowCarY+60):
        data.yellowCarSize = (130,160)
        data.nameColor,data.lineColor = "yellow","yellow"
        data.nameFont = "Helvetica 52 bold"
        data.redCar, data.blueCar = None,None
        data.isSelectedCar = Image.open("yellowCar.png")
        data.isGameStart = True
        
def keyPressed(event, data):
    
    if event.keysym == "s":
        data.isReady = True
    elif event.keysym == "p":
        if data.isMoving == True:
            data.isMenu = True
            data.isMoving = False
        elif data.isMenu == True:
            data.isMenu = False
            data.isMoving = True
    elif event.keysym == "o":
        data.isGameOver = True
    elif event.keysym == "Up":
        if data.level < 4:
            data.level += 1
            data.speedSaved += 5
    elif event.keysym == "Down":
        if data.level > 1:
            data.level -= 1
            data.speedSaved -= 5

def timerFired(data):
    if data.isGameOver == True:
        return None
    elif data.isMoving == True:
        if data.isSpecial == True:
            data.speed = 30 + data.speedSaved + data.level*2
            data.special = 0
            data.time += 1
            data.score += 5 + data.level
            if data.time == data.freqItem:
                data.time = 0
                data.isSpecial = False  
        else:
            data.objectSpeed = data.objectSpeedSaved + data.level
            data.speed = data.speedSaved + data.level*2
            data.time += 1
            data.score += (1 + data.level)
            if data.time == 100:
                data.numItems = 1
                data.time = 0
        data.treeOneY += data.speed
        data.treeTwoY += data.speed
        data.treeThreeY += data.speed
        data.treeFourY += data.speed
        timerFiredObstacles(data)
        timerFiredItems(data)
        tiemrFiredScore(data)

def tiemrFiredScore(data):
    
    if data.score//1000 == 1:
        data.level = 2
    elif data.score//1000 == 2:
        data.level = 3
    elif data.score//1000 == 3:
        data.level = 4

        
def timerFiredObstacles(data):
    
    if data.isGameStart == True and data.isReady == True and data.isMoving:
        if len(data.obstacles) < data.numObs:
            updateObsValue(data)
            data.obstacles.append(data.obsType)
        for obs in data.obstacles:
            obs.onTimerFired(data)
            if obs.isCrashed(data):
                if data.isShield == True and data.isSpecial == False:
                    data.isShield = False
                elif data.isSpecial == False:
                    data.health -= 1
                    data.latestObs = obs.type
                updateObsValue(data)
                data.obstacles.remove(obs)
            elif obs.y + obs.moveY >= data.height:
                updateObsValue(data)
                data.obstacles.remove(obs)
                
def timerFiredItems(data):
    
    if data.isGameStart == True and data.isReady == True:
        if len(data.items) < data.numItems:
            updateItemsValue(data)
            data.items.append(data.itemType)
            data.numItems -= 1
        for item in data.items:
            item.onTimerFired(data)
            if item.isCrashed(data):
                item.effect(data)
                data.items.remove(item)
            elif item.y + item.moveY >= data.height:
                data.items.remove(item)
        

def drawStartScreen(canvas, data):
    
    canvas.create_rectangle(0,0,data.width,data.height, fill="grey8",width=0)
    back = Image.open("back6.jpg")
    back = back.resize((data.width,data.height))
    canvas.back = ImageTk.PhotoImage(back)
    canvas.create_image(data.width/2,data.height/2, image=canvas.back)
    drawStartRectangle(canvas,data)
    drawStartScreenText(canvas,data)
    redCar = data.redCar
    if redCar != None:
        redCar = redCar.resize(data.redCarSize)
        canvas.redCar = ImageTk.PhotoImage(redCar)
        canvas.create_image(data.redCarX,data.redCarY, image=canvas.redCar)
    blueCar = data.blueCar
    if blueCar != None:
        blueCar = blueCar.resize(data.blueCarSize)
        canvas.blueCar = ImageTk.PhotoImage(blueCar)
        canvas.create_image(data.blueCarX, data.blueCarY, image=canvas.blueCar)
    yellowCar = data.yellowCar
    if yellowCar != None:
        yellowCar = yellowCar.resize(data.yellowCarSize)
        canvas.yellowCar = ImageTk.PhotoImage(yellowCar)
        yellowX,yellowY = data.yellowCarX, data.yellowCarY
        canvas.create_image(yellowX,yellowY,image=canvas.yellowCar)
    
def drawStartScreenText(canvas, data):
    
    nameFont = data.nameFont
    name = "DETECT_OR"
    nameX = data.width/2
    nameY = data.height*2/5
    nameColor = data.nameColor
    canvas.create_text(nameX,nameY,text=name,font=nameFont,fill=nameColor)
    help = "Help"
    helpX,helpY=data.helpX,data.helpY
    helpFont = data.helpFont
    helpColor = data.helpColor
    #To check boundary of HELP Word(for clicking)
    #canvas.create_rectangle(helpX-30,helpY-10,helpX+30,helpY+10,fill="grey")
    canvas.create_text(helpX,helpY,text=help,font=helpFont,fill=helpColor)
   
def drawStartRectangle(canvas, data):
    
    redX,redY = data.width*2/4, data.height*2/4
    blueX,blueY = data.width*1/4, data.height*3/4
    yellowX,yellowY  = data.width*3/4, data.height*3/4
    Y = data.height*4/13
    lineColor = data.lineColor
    canvas.create_line(blueX,Y,yellowX,Y, fill=lineColor, width=3)
    canvas.create_rectangle(blueX,redY,yellowX,yellowY,width=3,outline=lineColor)
    canvas.create_line(redX,redY,redX,blueY, fill=lineColor, width=3)
    # canvas.create_line(yellowX,yellowY,redX,redY,fill=lineColor, width=4)

def cursorPositionStart(canvas, data):
    
    if data.useMotion == True:
        if(data.cursorX > data.helpX-30 and data.cursorX < data.helpX+30 and
            data.cursorY > data.helpY-10 and data.cursorY < data.helpY+20):
            data.helpFont = "Helvetica 24 bold"
        elif(data.cursorX > data.redCarX-30 and data.cursorX < data.redCarX+30 and
            data.cursorY > data.redCarY-60 and data.cursorY < data.redCarY+60):
            cursorPositionStartRedCar(data)
        elif(data.cursorX > data.blueCarX-30 and data.cursorX < data.blueCarX+30 and
            data.cursorY > data.blueCarY-60 and data.cursorY < data.blueCarY+60):
            data.blueCarSize = (130,160)
            data.nameColor,data.lineColor = "darkturquoise","darkturquoise"
            data.nameFont = "Helvetica 52 bold"
            data.redCar, data.yellowCar = None, None
        elif(data.cursorX>data.yellowCarX-30 and data.cursorX<data.yellowCarX+30 and
            data.cursorY >data.yellowCarY-60 and data.cursorY < data.yellowCarY+60):
            data.yellowCarSize = (130,160)
            data.nameColor,data.lineColor = "yellow","yellow"
            data.nameFont = "Helvetica 52 bold"
            data.redCar, data.blueCar = None,None
        else:
            cursorPositionStartElse(canvas, data)

def cursorPositionStartElse(canvas, data):
    
    data.redCarSize,data.blueCarSize= (100, 130),(100, 130)
    data.yellowCarSize = (100, 130)
    data.helpFont = "Helvetica 18 bold underline"
    data.nameFont = "Helvetica 50"
    data.nameColor,data.lineColor = "white","white"
    data.blueCar = Image.open("blueCar.png")
    data.yellowCar = Image.open("yellowCar.png")
    data.redCar = Image.open("redCar.png")
    
def cursorPositionStartRedCar(data):
    data.redCarSize = (130,160)
    data.nameColor,data.lineColor = "red","red"
    data.nameFont = "Helvetica 52 bold"
    data.blueCar,data.yellowCar  = None,None
        
def drawHelpScreen(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="grey1",width=0)
    canvas.create_image(data.width/2, data.height*5/6, image=canvas.redCar)
    canvas.create_image(data.width*1/4, data.height*5/6, image=canvas.blueCar)
    canvas.create_image(data.width*3/4, data.height*5/6,image=canvas.yellowCar)
    back = "Back"
    backFont = data.backFont
    backX,backY = data.backX,data.backY
    canvas.create_text(backX,backY,text=back,font=backFont,fill="white")
    back = "Back"
    backX,backY = data.backX,data.backY
    drawHelpScreenHelper(canvas, data)
    
def drawHelpScreenHelper(canvas, data):
    gameIntro = """
    About DECTECT_OR,\n
    _OR, suffix appended to words to create an agent noun,
    indicating a person who does something. 
    In DECTECT_OR, you become a person who detects danger.\n\n
    How To Play,\n
    - In Home Screen, SELECT your car to start.
    - Next, follow the instructions to learn how to control the car.
    - And then, make move by using both hands to avoid DANGER.
    - Now, BREAK the high score!!\n\n
    Special Feature Of Each Car,
    
          <More Lives>          <More Speed>           <More Items>
    """
    introX = data.width/2
    introY = data.height*3/7
    introFont = "Helvetica 16 bold"
    canvas.create_text(introX,introY,text=gameIntro,font=introFont,fill="white")
    
    
def cursorPostitionHelp(canvas, data):
    if(data.cursorX > data.backX-30 and data.cursorX < data.backX+30 and
        data.cursorY > data.backY-10 and data.cursorY < data.backY+20):
        data.backFont = "Helvetica 24 bold"
    else:
        data.backFont = "Helvetica 18 bold underline"


def opencvToTk(frame):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(image=pil_img)
    return tk_image

def cameraFired(data):
    """Called whenever new camera frames are available.

    Camera frame is available in data.frame. You could, for example, blur the
    image, and then store that back in data. Then, in drawCamera, draw the
    blurred frame (or choose not to).
    """
    
    # For example, you can blur the image.
    #data.frame = cv2.GaussianBlur(data.frame, (11, 11), 0)
    
            
def drawRectOnBlue(data):
    lower_blue = np.array([50, 60, 120])
    upper_blue = np.array([100, 255, 255])
    if data.frame is not None:
        hsv = cv2.cvtColor(data.frame, cv2.COLOR_BGR2HSV) #convert to HSV\\
        mask = cv2.inRange(hsv, lower_blue, upper_blue) #find pixels in range

        edged = cv2.Canny(hsv, 10, 250)
        _,cnt,_= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,cnt,-1,(0,255,0),3)
        for i in range(len(cnt)):
            x,y,w,h=cv2.boundingRect(cnt[i])
            if w > 70 and h > 70:
                cv2.rectangle(data.frame,(x,y),(x+w,y+h),(255,255,0), 2)

def drawRectOnRed(data):
    lower_red = np.array([140, 60, 130])
    upper_red = np.array([190, 255, 255])
    if data.frame is not None:
        hsv = cv2.cvtColor(data.frame, cv2.COLOR_BGR2HSV) #convert to HSV\\
        mask = cv2.inRange(hsv, lower_red, upper_red) #find pixels in range
        edged = cv2.Canny(hsv, 10, 250)
        _,cnt,_= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,cnt,-1,(0,255,0),3)
        for i in range(len(cnt)):
            x,y,w,h=cv2.boundingRect(cnt[i])
            if w > 70 and h > 70:
                cv2.rectangle(data.frame,(x,y),(x+w,y+h),(255,0,255), 2)
                
def drawCamera(canvas, data):
    _, data.frame = data.camera.read()
    data.frame = cv2.flip(data.frame,1)
    cameraFired(data)
    drawRectOnBlue(data)
    drawRectOnRed(data)
    data.tk_image = opencvToTk(data.frame)
    canvas.create_image(data.width/2, data.height/2, image=data.tk_image)
    
    
def isBlueOn(data):
    
    #lower_blue = np.array([50, 50, 70])
    lower_blue = np.array([50, 60, 120])
    upper_blue = np.array([100, 255, 255])
    if data.frame is not None:
        hsv = cv2.cvtColor(data.frame, cv2.COLOR_BGR2HSV) #convert to HSV\\
        mask = cv2.inRange(hsv, lower_blue, upper_blue) #find pixels in range

        edged = cv2.Canny(hsv, 10, 250)
        _,cnt,_= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,cnt,-1,(0,255,0),3)
        for i in range(len(cnt)):
            x,y,w,h=cv2.boundingRect(cnt[i])
            if w > 70 and h > 70:
                return True
        return False

def isRedOn(data):
    
    lower_red = np.array([140, 60, 130])
    upper_red = np.array([190, 255, 255])
    if data.frame is not None:
        hsv = cv2.cvtColor(data.frame, cv2.COLOR_BGR2HSV) #convert to HSV\\
        mask = cv2.inRange(hsv, lower_red, upper_red) #find pixels in range
        edged = cv2.Canny(hsv, 10, 250)
        _,cnt,_= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,cnt,-1,(0,255,0),3)
        for i in range(len(cnt)):
            x,y,w,h=cv2.boundingRect(cnt[i])
            if w > 70 and h > 70:
                return True
        return False
    
    
def detector(data):
    _, data.frame = data.camera.read()
    data.frame = cv2.flip(data.frame,1)
    data.tk_image = opencvToTk(data.frame)
    if isRedOn(data) and isBlueOn(data) and data.isMenu == False:
        data.isMoving = True
    elif isRedOn(data) == True and data.isMoving and data.isMenu == False:
        if data.carX >= data.width/4:
            data.carX -= 20
    elif isBlueOn(data) == True and data.isMoving and data.isMenu == False:
        if data.carX <= data.width*3/4:
            data.carX += 20
    else:
        if data.isMoving == True:
            if data.special == data.maxSpecial:
                data.time = 0
                data.isSpecial = True
   
def drawCar(canvas, data):
    
    car = data.isSelectedCar
    if car == data.redCar:
        data.speedSaved = 15
    elif car == data.yellowCar:
        data.freqItem = 100
    if data.health== 0:
        data.isGameOver = True
    carSize = data.carSize
    car = car.resize(carSize)
    canvas.car = ImageTk.PhotoImage(car)
    canvas.create_image(data.carX,data.carY, image=canvas.car)

def drawField(canvas, data):
    
    if data.level == 1:
        data.backColor= "darkkhaki"
        data.roadColor = "khaki"
    elif data.level == 2:
        data.backColor= "darkseagreen"
        data.roadColor = "lightgreen"
    elif data.level == 3:
        data.backColor= "mediumorchid"
        data.roadColor = "orchid"
    elif data.level == 4:
        data.backColor= "darkslateblue"
        data.roadColor = "slateblue"
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.backColor,width=0)
    canvas.create_rectangle(data.width/5,0,data.width*4/5,data.height,fill=data.roadColor,width=0)
    canvas.create_line(data.width*18/80,0,data.width*18/80,data.height, fill="white", width=5)
    canvas.create_line(data.width*62/80,0,data.width*62/80,data.height, fill="white", width=5)

def drawTree(canvas, data):
    maxY = 870
    lineLength = 60
    minY = 70
    lineColor = "gold"
    if data.level == 1:
        trees = ["Trees/tree3.png","Trees/tree1.png", "Trees/tree5.png","Trees/tree6.png"]
    elif data.level == 2:
        trees = ["Trees/brownTree.png","Trees/brownTree2.png", "Trees/brownTree3.png","Trees/emptyTree.png"]
    elif data.level == 3:
        trees = ["Trees/pinkTree1.png","Trees/pinkTree2.png", "Trees/pinkTree3.png","Trees/pinkTree2.png"]
    elif data.level == 4:
        trees = ["Trees/greenTree2.png","Trees/greenTree3.png", "Trees/greenTree4.png","Trees/greenTree5.png"]
    if data.numOne == None:
        data.numOne = random.randrange(0,4)
    elif data.treeOneY > maxY:
        data.numOne = random.randrange(0,4)
        data.treeOneY = -minY
    treeOne = Image.open(trees[data.numOne])
    canvas.treeOne = ImageTk.PhotoImage(treeOne)
    canvas.create_image(data.width/10,0+data.treeOneY, image=canvas.treeOne)
    canvas.create_image(data.width*9/10,0+data.treeOneY, image=canvas.treeOne)
    canvas.create_line(data.width/2,-lineLength+data.treeOneY, data.width/2, 
    lineLength+data.treeOneY, fill=lineColor, width=15)
    if data.numTwo == None:
        data.numTwo = random.randrange(0,4)
    elif data.height/3+data.treeTwoY > maxY:
        data.numTwo = random.randrange(0,4)
        data.treeTwoY = -data.height/3 -minY
    treeTwo = Image.open(trees[data.numTwo])
    canvas.treeTwo = ImageTk.PhotoImage(treeTwo)
    canvas.create_image(data.width/10,data.height/3+data.treeTwoY, image=canvas.treeTwo)
    canvas.create_image(data.width*9/10,data.height/3+data.treeTwoY, image=canvas.treeTwo)
    canvas.create_line(data.width/2,data.height/3-lineLength+data.treeTwoY, 
    data.width/2, data.height*1/3+lineLength+data.treeTwoY, fill=lineColor, width=15)
    if data.numThree == None:
        data.numThree = random.randrange(0,4)
    elif data.height*2/3+data.treeThreeY > maxY:
        data.numThree = random.randrange(0,4)
        data.treeThreeY = -data.height*2/3-minY
    treeThree = Image.open(trees[data.numThree])
    canvas.treeThree = ImageTk.PhotoImage(treeThree)
    canvas.create_image(data.width/10,data.height*2/3+data.treeThreeY, image=canvas.treeThree)
    canvas.create_image(data.width*9/10,data.height*2/3+data.treeThreeY, image=canvas.treeThree)
    canvas.create_line(data.width/2,data.height*2/3-lineLength+data.treeThreeY, 
    data.width/2, data.height*2/3+ lineLength+data.treeThreeY, fill=lineColor, width=15)
    if data.numFour == None:
        data.numFour= random.randrange(0,4)
    elif data.height+data.treeFourY > maxY :
        data.numFour= random.randrange(0,4)
        data.treeFourY = -data.height-minY
    treeFour = Image.open(trees[data.numFour])
    canvas.treeFour = ImageTk.PhotoImage(treeFour)
    canvas.create_image(data.width/10,data.height+data.treeFourY, image=canvas.treeFour)
    canvas.create_image(data.width*9/10,data.height+data.treeFourY, image=canvas.treeFour)
    canvas.create_line(data.width/2,data.height-lineLength+data.treeFourY, 
    data.width/2, data.height+ lineLength+data.treeFourY, fill=lineColor, width=15)
    
class Obstacles(object):
    
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.speed = data.objectSpeed
        self.moveY = 0
        self.radius = 25
        
    def onTimerFired(self, data):
        pass
    
    def draw(self, data, canvas):
        pass
        
    def isCrashed(self, data):
        for points in data.carPointsObs:
            carX,carY = points
            # center of obstacles
            centerX = self.x
            centerY = self.y + self.moveY
            if (carX - centerX)**2 + (carY - centerY)**2 <= self.radius**2:
                return True
        return False
        
class Instagram(Obstacles):
    
    def __init__(self, x, y, data):
        super().__init__(x,y, data)
        self.name = "Obstacles/instagram.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((80,80))
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.move = 3
        self.initX = x
        self.type = "Instagram"

    def onTimerFired(self,data):
        self.x += self.move
        if self.x >= data.width*4/5:
            self.x = data.width/5
        if data.isMoving == True:
            self.moveY += self.speed
    
    def draw(self, data,  canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)
        
class Mail(Obstacles):
    
    def __init__(self,x,y, data):
        super().__init__(x,y, data)
        self.name = "Obstacles/mail.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((110,110))
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.initX = self.x
        self.move = 3
        self.type = "Mail"
        
    def onTimerFired(self,data):
        self.y += self.move
        if data.isMoving == True:
            self.moveY += self.speed
            
    def draw(self, data, canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)
        
class Youtube(Obstacles):
    
    def __init__(self, x, y, data):
        super().__init__(x,y, data)
        self.name = "Obstacles/youtube.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((75,75))
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.type = "Youtube"
        
    def onTimerFired(self, data):
        self.y += 3
        self.x = 200 * (math.sin(self.y/30)) + 400
        if data.isMoving == True:
            self.moveY += self.speed

    def draw(self, data, canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)
    
class Facebook(Obstacles):
    
    def __init__(self, x, y, data):
        super().__init__(x,y, data)
        self.name = "Obstacles/facebook.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((75,75))
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.theta = 0
        self.bigRadius = 180 
        self.type = "Facebook"
        
    def onTimerFired(self, data):
        self.theta += 1/13
        self.x = self.bigRadius*math.cos(self.theta) + 400
        self.y = self.bigRadius*math.sin(self.theta)
        if data.isMoving == True:
            self.moveY += self.speed
        
    def draw(self, data, canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)
        
        
class Phone(Obstacles):
    
    def __init__(self,x,y, data):
        super().__init__(x,y, data)
        self.name = "Obstacles/phone.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((80,80))
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.newSize = 80
        self.time = 0
        self.type = "Phone"
        
    def onTimerFired(self, data):
        newSize =  self.newSize
        self.image = self.image.resize((newSize,newSize))
        self.imageTk = ImageTk.PhotoImage(self.image)
        if newSize == 80 and self.time == 20:
            self.newSize = 150
            self.time = 0
            self.radius = 60
        elif newSize == 150 and self.time == 20:
            self.newSize = 80
            self.time = 0
            self.radius = 30
        self.time += 1
        if data.isMoving == True:
            self.moveY += self.speed
        
    def draw(self, data, canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)   
        
        
def updateObsValue(data):
    obsXMin = data.width*3/10
    obsXMax = data.width*7/10
    obsXDiff = 20
    obsX = random.randrange(obsXMin, obsXMax, obsXDiff)
    numObs = random.randrange(0,5)
    if numObs == 0: data.obsType = Instagram(obsX,0, data)
    elif numObs == 1: data.obsType = Mail(obsX,0, data)
    elif numObs == 2: data.obsType = Facebook(obsX,0, data)
    elif numObs == 3: data.obsType = Phone(obsX,0, data)
    elif numObs == 4: data.obsType = Youtube(obsX,0, data)


def carPoints(data,canvas):
    # update points of cars in list form to use whether point touches obstacles
    carWidth, carHeight = 20 ,45
    carX, carY = data.carX, data.carY 
    northWest = (carX-carWidth, carY-carHeight)
    northEast =  (carX+carWidth,carY-carHeight)
    west = (carX-carWidth, carY)
    east =  (carX+carWidth, carY)
    southWest = (carX-carWidth, carY + carHeight)
    southEast = (carX+carWidth, carY + carHeight)
    data.carPointsObs = [northWest, northEast, west, east]
    data.carPointsItem = [northWest, northEast, southWest, southEast,west,east]
   

class Item(object):
    def __init__(self,x,y,data):
        self.x = x
        self.y = y
        self.moveY = 0
        self.speed = data.objectSpeed
        self.radius = 30

    def isCrashed(self, data):
        for points in data.carPointsItem:
            carX,carY = points
            # center of obstacles
            centerX = self.x
            centerY = self.y + self.moveY
            if (carX - centerX)**2 + (carY - centerY)**2 <= self.radius**2:
                print(self.name)
                return True
        return False
        
    def onTimerFired(self, data):
        if data.isMoving == True:
            self.moveY += data.objectSpeed
            
    def draw(self, data, canvas):
        canvas.create_image(self.x,self.y+self.moveY, image=self.imageTk)
        
class TaroItem(Item):
    def __init__(self, x, y,data):
        super().__init__(x,y,data)
        self.name = "Items/taro.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((130,130))
        self.imageTk = ImageTk.PhotoImage(self.image)
        
    def effect(self,data):
        if data.special < data.maxSpecial:
            data.special += 1

class LimeItem(Item):
    def __init__(self, x, y,data):
        super().__init__(x,y,data)
        self.name = "Items/lime.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((130,130))
        self.imageTk = ImageTk.PhotoImage(self.image) 
        
    def effect(self,data):
        data.obstacles = []
        
class MochaItem(Item):
    def __init__(self, x, y,data):
        super().__init__(x,y,data)
        self.name = "Items/mocha.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((130,130))
        self.imageTk = ImageTk.PhotoImage(self.image)
        
    def effect(self,data):
        data.isShield = True
        
class OrangeItem(Item):
    def __init__(self, x, y,data):
        super().__init__(x,y,data)
        self.name = "Items/orange.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((130,130))
        self.imageTk = ImageTk.PhotoImage(self.image)
        
    def effect(self,data):
        pass
        
        
class RedBerryItem(Item):
    def __init__(self, x, y,data):
        super().__init__(x,y,data)
        self.name = "Items/redBerry.png"
        self.image = Image.open(self.name) 
        self.image = self.image.resize((130,130))
        self.imageTk = ImageTk.PhotoImage(self.image)
        
    def effect(self,data):
        if data.health < data.maxHealth:
            data.health += 1
        
def updateItemsValue(data):
    itemXMin = data.width*3/10
    itemXMax = data.width*7/10
    itemXDiff = 20
    itemX = random.randrange(itemXMin, itemXMax, itemXDiff)
    numItems = random.randrange(0,5)
    if numItems == 0: data.itemType = TaroItem(itemX,0,data)
    elif numItems == 1: data.itemType = LimeItem(itemX,0,data)
    elif numItems == 2: data.itemType = OrangeItem(itemX,0,data)
    elif numItems == 3: data.itemType = RedBerryItem(itemX,0,data)
    elif numItems == 4: data.itemType = MochaItem(itemX,0,data)

def drawScoreBoard(canvas, data):
    data.numObs = 2+data.level
    canvas.create_rectangle(0,0,data.width,data.height/15,
    fill="lightcyan",width=0, outline = "beige")
    menuText = "press (p) to Pause/Play"
    canvas.create_text(data.width*13/15, data.height/30, text=menuText,
    font="Helvetica 13 bold", fill="dimgray")
    scoreText = data.score
    canvas.create_text(data.width/2, data.height/7, text=scoreText,
    font="Helvetica 40 bold", fill="black")
    name = "heartTwo.png"
    hpX, hpY = data.width/20, data.height/30
    image = Image.open(name) 
    image = image.resize((30,30))
    canvas.imageTk = ImageTk.PhotoImage(image)
    for i in range(data.health):
        canvas.create_image(hpX,hpY, image=canvas.imageTk)
        hpX += 50
    name = "special.png"
    starX, starY = 450, data.height/30
    image = Image.open(name) 
    image = image.resize((40,40))
    canvas.special = ImageTk.PhotoImage(image)
    for i in range(data.special):
        canvas.create_image(starX,starY, image=canvas.special)
        starX += 50
  
def drawItem(canvas, data):
    if data.isSpecial == True:
        rocket = Image.open("rocket.png")
        canvas.rocket = ImageTk.PhotoImage(rocket)
        canvas.create_image(data.carX,data.carY, image=canvas.rocket)
    elif data.isShield == True:
        shield = Image.open("shield.png")
        shield = shield.resize((100,100))
        canvas.shield = ImageTk.PhotoImage(shield)
        canvas.create_image(data.carX,data.carY, image=canvas.shield)
    
    
def dodgeObs(obsList, path=None):
    
    if len(obsList) == 0:
        return path
    else:
        obs = obsList[0]
        if isLegal(right, path):
            obsList.pop(0)
            solution = dodgeObs(obsList, path, obs)
            if solution != None:
                return solution
            else:
                obsList.insert(0,obs)
        if isLegal(left, path):
            obsList.pop(0)
            solution = dodgeObs(obsList, path, obs)
            if solution != None:
                return solution
            else:
                obsList.insert(0,obs)
        return None
        


            
def drawGetReady(canvas, data):
    if data.isSelectedCar == data.blueCar:
        data.health, data.maxHealth = 8,8
    canvas.create_rectangle(0,data.height/3,data.width,data.height*2/3, fill="lightcyan", width=0)
    readyText = "READY!"
    canvas.create_text(data.width/2,data.height*3/7,text=readyText,fill="dimgray",font ="Helvetica 44 bold" )
    readyText = "Put up BOTH Red and Blue to start"
    canvas.create_text(data.width/2,data.height*4/7,text=readyText,fill="dimgray",font ="Helvetica 24 bold" )

def drawMenu(canvas, data):
    name = "sleep.png"
    starX, starY = data.width/2, data.height/2
    image = Image.open(name) 
    canvas.power = ImageTk.PhotoImage(image)
    canvas.create_image(starX,starY, image=canvas.power)

def drawGameOver(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height,width=0,fill="red")
    name = "skull.png"
    starX, starY = data.width/2, data.height/2
    image = Image.open(name) 
    canvas.skull = ImageTk.PhotoImage(image)
    canvas.create_image(starX,starY, image=canvas.skull)
    text = "You've DIED using:"
    canvas.create_text(data.width/2,data.height/6,text=text,font="Helvetica 40 bold",fill="white")
    text = "%s"%data.latestObs
    canvas.create_text(data.width/2,data.height*2/7,text=text,font="Helvetica 50 bold",fill="white")
    text ="""
    '3,500 people were killed in crashes involving distracted drivers'(NHTS)
     Before detecting DANGER approaching outside, prevent from inside .
    """
    canvas.create_text(data.width/2,data.height*3/4,text=text,font="Helvetica 16 bold",fill="white")
    text = "%d"%data.score
    canvas.create_text(data.width/2,data.height*6/7,text=text,font="Helvetica 50 bold",fill="white")
    
def drawTutorial(canvas, data):
    text = data.tutorialText
    canvas.create_text(data.width/2,data.height/10,text=text,font="Helvetica 20 bold",fill="black")
    if isRedOn(data):
        data.tutorialText = "Good Job! Now show only blue to move left"
    elif isBlueOn(data):
        data.tutorialText = "Nice! Now hide both to use special ability"
    elif data.tutorialText == "Nice! Now hide both to use special ability":
        data.tutorialText = "Great! Now press 's' to start the game"
    text = "Press 's' to skip the tutorial"
    canvas.create_text(data.width*8/10,data.height*9/10,text=text,font="Helvetica 15 bold",fill="black")


def redrawAll(canvas, data):
    #draw in canvas
    if data.isGameStart == False and data.isHelp == False:
        cursorPositionStart(canvas, data)
        drawStartScreen(canvas, data)
    elif data.isGameStart == False and data.isHelp == True:
        cursorPostitionHelp(canvas, data)
        drawHelpScreen(canvas, data)
    elif data.isGameStart == True and data.isReady == False:
        data.useMotion = False
        drawCamera(canvas, data)
        drawTutorial(canvas, data)
    elif data.isGameOver:
        drawGameOver(canvas,data)
    elif data.isGameStart == True and data.isReady == True:
        cv2.imshow("Cam", data.frame)
        detector(data)
        carPoints(data,canvas)
        drawField(canvas,data)
        drawTree(canvas, data)
        drawCar(canvas, data)
        for item in data.items:
            item.draw(data,canvas)
        for obs in data.obstacles:
            obs.draw(data, canvas)
        drawItem(canvas, data)
        drawScoreBoard(canvas, data)
        if data.isMenu == True:
            drawMenu(canvas, data)
        elif data.isMoving == False:
            drawGetReady(canvas, data)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()   

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    def mouseMotionWrapper(event, canvas, data):
        if data.useMotion == True:
            mouseMotion(event, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.cameraIndex = 0
    camera = cv2.VideoCapture(data.cameraIndex)
    data.camera = camera
    data.timerDelay = 3 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event:
                            mouseMotionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    data.camera.release()
    print("bye!")



if __name__ == "__main__":
    run(800, 750)