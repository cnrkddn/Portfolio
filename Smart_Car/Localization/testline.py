#!/usr/bin/env python3
import sys
sys.path.append('../')
import robot as rb
import time 
import signal 

robot = rb.Robot(wheelbase=7.25, radius=1.625)

def signal_handler(sig, frame):
    robot.stop()
    sys.exit(0)

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

