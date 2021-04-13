#!/usr/bin/env python3

import robot as rob
import time

def main():
    robot = rob.Robot()
    lastTime = time.time()
    while (True):
        currTime = time.time()
        print(robot.get_enc_radians())
        robot.update_robot_odometry(currTime - lastTime)
        print(robot.odom.x, robot.odom.y, robot.odom.theta)
        lastTIme = currTime
        time.sleep(0.5)


if __name__ == '__main__':
    main()

