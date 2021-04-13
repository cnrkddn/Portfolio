#!/usr/bin/env python3
import sys
sys.path.append('../')
import time
import robot as rb
# import matplotlib.pyplot as plt
import math 
import signal

# forward (positive) = towards sensor 1
# backward (negative) = towards sensor 2
# sensor gets smaller as it get closer to ground
# direction is ok for now

robot = rb.Robot(wheelbase=7.125, radius=1.625)

def signal_handler(sig, frame):
    robot.stop()
    sys.exit(0)

def pid_rot_tuning_right(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 3.5
    Kpl = 3.5
    targetV = 0
    targetW = math.pi
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = -37
    powR = 37
    while (currTime - startTime <= 0.5):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())
            nowTime = currTime
            print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def pid_rot_tuning_left(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 1.25
    Kpl = 1.25
    targetV = 0
    targetW = -math.pi
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = 37
    powR = -37
    while (currTime - startTime <= 0.5):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())
            nowTime = currTime
            print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def pid_straight_tuning(robot):
    # tuning the velocity to be 0.75, w to be 0
    Kpr = 7
    Kpl = 6.5
    targetV = 4
    targetW = 0
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = nowTime
    powL = 25
    powR = 25
    while (currTime - startTime <= 0.5):
        currTime = time.time() 
        if (first):
            first = False
        else:
            dt = currTime - nowTime
            pows = robot.pid_Vw(targetV, targetW, Kpl, Kpr, dt) 
            robot.update_odometry(dt)
            print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())
            nowTime = currTime
            print(pows)
            robot.drive_robot_power(powL + pows[0], powR + pows[1]) 
        time.sleep(0.05)
    robot.stop()

def test_encoder(robot):
    while (True):
        print(robot.get_encoder_readings())
        time.sleep(0.1)

def test_odom(robot):
    nowTime = time.time()
    first = True
    while (True):
        if (first):
            first = False
        else:    
            dt = time.time() - nowTime
            robot.update_odometry(dt)
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
        time.sleep(0.1)

def test_driven_odom(robot, powL, powR):
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = 0
    while (True):
        currTime = time.time() 
        if (first):
            first = False

        else:    
            dt = currTime - nowTime
            robot.update_odometry(dt)
            print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())

        robot.drive_robot_power(powL, powR)
        # powL = -powL
        # powR = -powR
        nowTime = currTime
        time.sleep(0.1)

def test_sequence_odom(robot, powList):
    for item in powList:
        nowTime = time.time()
        startTime = nowTime
        first = True
        currTime = nowTime
        powL = item[0]
        powR = item[1]
        while (currTime - startTime < 5):
            currTime = time.time() 
            robot.drive_robot_power(powL, powR)
            if (first):
                first = False
            else:
                dt = currTime - nowTime
                robot.update_odometry(dt)
                # print('Time %.3f' % (currTime - startTime))
                # print('Odom', robot.get_odometry())
                # print('Displacement of L, R', robot.get_wheel_displacement())
                # print('Enc Readgins', robot.get_encoder_readings())
                nowTime = currTime
            time.sleep(0.05)
        robot.stop()
        print('Odom', robot.get_odometry())
        print('Displacement of L, R', robot.get_wheel_displacement())
        print('Enc Readgins', robot.get_encoder_readings())
        print('\n')
        time.sleep(5)
 
    robot.stop()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    robot.stop()
    time.sleep(1)
    test_enc = False
    test_od = False
    test_drOd = False
    test_seq = True
    tune_pid = False
    tune_turnL = False
    tune_turnR = False
    dataX = []
    dataY = []
    dataTh = []
    speedList = [[-25, 25], [-10, 10], [20, 20], [10, 30], [20, -10]]
    if (test_enc):
        test_encoder(robot)
    elif (test_od):
        test_odom(robot)
    elif (test_drOd):
        test_driven_odom(robot, 17, 17)
    elif (test_seq):
        test_sequence_odom(robot, speedList)
    elif (tune_pid):
        pid_straight_tuning(robot)
    elif (tune_turnL):
        pid_rot_tuning_left(robot)
    elif (tune_turnR):
        pid_rot_tuning_right(robot)
    plt.plot(dataX, dataY)
    plt.show()



if __name__ == '__main__':
        main()
