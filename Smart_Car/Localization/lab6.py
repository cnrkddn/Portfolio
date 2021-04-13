#!/usr/bin/env python3
import sys
sys.path.append('../')
import robot as rb
import time 
import signal 
import numpy as np
import matplotlib.pyplot as plt 
import math
import copy

robot = rb.Robot(wheelbase=7.25, radius=1.625)
ang_list = [math.pi/8 * i for i in range(16)]

def convert_angle(ang):
    return math.atan2(math.sin(ang), math.cos(ang))

def signal_handler(sig, frame):
    robot.stop()
    sys.exit(0)

def generate_gaussian_prob(mean, std, x):
    k = 1 / (math.sqrt((2 * math.pi * std**2)))
    ePart = np.exp((-(x - mean)**2) / (2 * std**2))
    return k * ePart

def normalize(prob_map):
    total = sum(prob_map)
    return [item / total for item in prob_map]

def update_transition_probabilities(prob_map, odom_theta, started=True):
    # odom theta should be mod 2 * pi
    if (not started):
        return []
    new_prob_map = []
    std = 0.1
    for i in range(len(prob_map)):
        # shift the mean by odom_theta
        gaussian_mean = convert_angle(ang_list[i] - odom_theta)
        # print(gaussian_mean)
        temp_map = np.zeros(len(prob_map))
        for j in range(len(prob_map)):
            proper_angle = convert_angle(ang_list[j])
            # print(proper_angle)
            temp_map[j] = prob_map[j] * generate_gaussian_prob(gaussian_mean, std, proper_angle)
        # print(temp_map)
        new_prob_map.append(sum(temp_map))
    # real_prob_map = [sum(item) for item in new_prob_map]
    # print(real_prob_map)
    return normalize(new_prob_map)


def update_observation_probabilities(prob_map, obs, bitVec, started=True):
    bitVec = np.array(bitVec)
    zeroIndices = np.where(bitVec == 0)
    oneIndices = np.where(bitVec == 1)
    new_prob_map = copy.deepcopy(prob_map)
    prob_vec = np.zeros(len(prob_map))
    if (not obs):
        prob_vec[zeroIndices] = 0.95
        prob_vec[oneIndices] = 0.05
    else:
        prob_vec[zeroIndices] = 0.3
        prob_vec[oneIndices] = 0.7
    new_prob_map = np.multiply(new_prob_map, prob_vec)
    return normalize(new_prob_map) 

# turns to the right in order to find the line
def find_line_right(robot):
        lightThresh = 2200 # insert some threshold number, play around with it
        lightSensed = robot.get_sensor(1)
        while(lightSensed < lightThresh):
                robot.drive_robot_power(-20, 20)
                time.sleep(0.05)
                lightSensed = robot.get_sensor(1)
                # print(lightSensed)
        # print('Sensed Line: ' + str(lightSensed))
        robot.stop()
        return lightSensed

def calibrate(robot):
    while (True):
        print(robot.get_sensor(2))
        time.sleep(0.5)

def calibrate_ultrasonic(robot):
    time.sleep(5)
    while(True):
        print(robot.get_sensor(1))
        time.sleep(0.5)

def main():
        robot.stop()
        signal.signal(signal.SIGINT, signal_handler)
        robot.set_sensor(2, 'light')
        robot.set_sensor(1, 'ultrasonic')
        time.sleep(1)
        baseLight = 2300 # figure out the line's sensor reading by observation
        baseSpeed = [20, 20]
        # use calibrate only if checking sensor values
        # calibrate(robot)
        calibrate_ultrasonic(robot)
        # lightSensor = find_line_right(robot)
        kp = 0.15 # figure out this value later
        kd = 0.0000 # gotta tune this value
        # rotates to the right
        lastErr = 0
        first = True
        nowTime = time.time()
        startTime = nowTime
        currTime = nowTime
        while (currTime - startTime < 80):
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
                lightSensed = robot.get_sensor(2)
                # print(lightSensed)
                err = (lightSensed - baseLight)
                pControl = err * kp
                newPowLeft = baseSpeed[0] + (pControl)
                newPowRight = baseSpeed[1] - (pControl)
                robot.drive_robot_power(newPowLeft, newPowRight)
                nowTime = currTime
            time.sleep(0.05)
                

if __name__ == '__main__':
        main()

