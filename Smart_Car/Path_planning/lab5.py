import sys
sys.path.append('../')
import time
import robot as rb
import wavefront as wv
# import matplotlib.pyplot as plt
import math 

#four inches, set rampTime to be 
def ramp_velocity(Vmax, t, rampTime):
    fullT = 0.5 + 2 * rampTime
    if (t <= rampTime):
        return Vmax * t / rampTime
    elif (t > fullT - rampTime):
        dt = fullT - t
        # print(dt)
        return Vmax * dt / rampTime 
    else:
        return Vmax

def pid_rot_tuning_round(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 2 
    Kpl = 2
    targetV = 0
    rampTime = 0.15
    targetW = 2 * math.pi
    targetT = 0.2
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = -70
    powR = 70
    while (currTime - startTime <= targetT + 2 * rampTime):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            targetW = math.pi
            targetW = ramp_velocity(targetW, currTime - startTime, rampTime)
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            ''' print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings()) '''
            nowTime = currTime
            # print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()



def pid_rot_tuning_right(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 0.25
    Kpl = 0.25
    targetV = 0
    rampTime = 0.15
    targetW = math.pi / 2
    targetT = 0.2
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = -22
    powR = 22
    while (currTime - startTime <= targetT + 2 * rampTime):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            targetW = math.pi
            targetW = ramp_velocity(targetW, currTime - startTime, rampTime)
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            ''' print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings()) '''
            nowTime = currTime
            # print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def pid_rot_tuning_left(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 0.25
    Kpl = 0.25
    targetV = 0
    targetW = (-math.pi / 2) 
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = 22
    powR = -22
    targetT = 0.2
    rampTime = 0.15
    while (currTime - startTime <= targetT + 2 * rampTime):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            targetW = -math.pi
            targetW = ramp_velocity(targetW, currTime - startTime, rampTime)
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            ''' print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())'''
            nowTime = currTime
            # print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.025)
    robot.stop()

def pid_diag_tuning(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 1.5
    Kpl = 1.5
    targetV = 5.65
    targetW = 0
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = 37
    powR = 37
    rampTime = 0.15
    targetT = 0.2
    while (currTime - startTime <= targetT + 2 * rampTime):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            targetV = 5.65
            targetV = ramp_velocity(targetV, currTime - startTime, rampTime)
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            ''' print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())'''
            nowTime = currTime
            # print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def pid_straight_tuning(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 1.5
    Kpl = 1.5
    targetV = 4
    targetW = 0
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = 25
    powR = 25
    rampTime = 0.15
    targetT = 0.2
    while (currTime - startTime <= targetT + 2 * rampTime):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            targetV = 4
            targetV = ramp_velocity(targetV, currTime - startTime, rampTime)
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            ''' print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())'''
            nowTime = currTime
            # print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def main_loop(xstart, ystart, xgoal, ygoal, convert=False):
        robot = rb.Robot(wheelbase=3.75, radius=1.125)
        robot.stop()
        path = wv.full_path_4point(xstart, ystart, xgoal, ygoal, convertInput=convert)
        print(path)
        time.sleep(1)
        for waypoint in path:
            distance = waypoint[0]
            theta = waypoint[1]
            if (distance == 1):
                pid_straight_tuning(robot)
            time.sleep(0.35)
            if (theta == math.pi):
                pid_rot_tuning_left(robot)
                time.sleep(0.375)
                pid_rot_tuning_left(robot)
                time.sleep(0.375)
            elif (theta == math.pi / 2):
                pid_rot_tuning_right(robot)
                time.sleep(0.65)
            elif (theta == - math.pi / 2):
                pid_rot_tuning_left(robot)
                time.sleep(0.65)
        robot.stop()

def in_neighbor(ang):
    angs = [0, math.pi/4, math.pi/2, 3 * math.pi / 4, math.pi, -math.pi/4, -math.pi/2, -3 * math.pi / 4]
    for angle in angs:
        if ((ang - angle)**2) < 0.01:
            return angle

    

def main_loop8(xstart, ystart, xgoal, ygoal, convert=False):
        robot = rb.Robot(wheelbase=3.75, radius=1.125)
        robot.stop()
        path = wv.full_path_8point(xstart, ystart, xgoal, ygoal, convertInput=convert)
        print(path)
        time.sleep(1)
        for waypoint in path:
            distance = waypoint[0]
            theta = waypoint[1]
            if (distance == 1):
                pid_straight_tuning(robot)
            elif (distance == 2):
                pid_diag_tuning(robot)
            time.sleep(0.35)
            theta = in_neighbor(theta)
            if (theta == -math.pi / 4):
                pid_rot_tuning_left(robot)
                time.sleep(0.65)
            elif (theta == -math.pi / 2):
                pid_rot_tuning_left(robot)
                time.sleep(0.375)
                pid_rot_tuning_left(robot)
                time.sleep(0.375)
            elif(theta == -3 * math.pi / 4):
                pid_rot_tuning_left(robot)
                time.sleep(0.65/3)
                pid_rot_tuning_left(robot)
                time.sleep(0.65/3)
                pid_rot_tuning_left(robot)
                time.sleep(0.65/3)
            elif (theta == math.pi / 4):
                pid_rot_tuning_right(robot)
                time.sleep(0.65)
            elif (theta == math.pi / 2):
                print(theta)
                pid_rot_tuning_right(robot)
                time.sleep(0.375)
                pid_rot_tuning_right(robot)
                time.sleep(0.375)
            elif(theta == 3 * math.pi / 4):
                pid_rot_tuning_right(robot)
                time.sleep(0.65/3)
                pid_rot_tuning_right(robot)
                time.sleep(0.65/3)
                pid_rot_tuning_right(robot)
                time.sleep(0.65/3)
            elif (theta == math.pi):
                pid_rot_tuning_left(robot)
                time.sleep(0.65/4)
                pid_rot_tuning_left(robot)
                time.sleep(0.65/4)
                pid_rot_tuning_left(robot)
                time.sleep(0.65/4)
                pid_rot_tuning_left(robot)
                time.sleep(0.65/4)
        robot.stop()

# path = wv.full_path_4point(36, 14, 33, 17, convertInput=True)
