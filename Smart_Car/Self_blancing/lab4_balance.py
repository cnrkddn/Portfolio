#!/usr/bin/env python3

# forward (positive) = towards sensor 1
# backward (negative) = towards sensor 2
# sensor gets smaller as it get closer to ground
# direction is ok for now

import sys
import signal
sys.path.append('../')
import robot as rob
import time

errorData = []

def signal_handler(sig, frame):
        if (not (len(errorData) == 0)):
                with open('data.txt', 'w') as fi:
                        fi.write('\n'.join('%s %s %s %s %s' % item for item in errorData))
                print("File written!")
        else:
            print("No data!")
        robot.stop()
        sys.exit(0)

def startBot():
    robot = rob.Robot()
    robot.stop()
    robot.set_sensor(1, 'light') # potentiall change the port numbers later
    robot.set_sensor(2, 'light') # potentially change the port numbers later
    time.sleep(1)
    return robot

robot = startBot()

def test_sensors(robot):
        while (True):
                print('Sensor 1: ' + str(robot.get_sensor(1)))
                print('Sensor 2: ' + str(robot.get_sensor(2)))
                time.sleep(0.5)

def check_motor_direction(robot):
        while(True):
                print("forward")
                robot.drive_robot_power(10, 10)
                time.sleep(3)
                robot.stop()
                time.sleep(1)
                print("backwards")
                robot.drive_robot_power(-10, -10)
                time.sleep(3)



def main():
        robot.print_status()
        test_sense = False
        test_motor = False
        signal.signal(signal.SIGINT, signal_handler)
        Kp = 0.725
        Kd = 0.01
        Ki = 4.75
        lastError = 0
        first = True
        DError = 0
        IError = 0
        lastTime = 0
        recordTime = 0
        base = 17
        if (test_sense):
                test_sensors(robot)
        if (test_motor):
                check_motor_direction(robot)
        while (True):
                currTime = time.time()
                sensor1 = robot.get_sensor(1)
                sensor2 = robot.get_sensor(2)
                sensorError = sensor2 - sensor1 - base# double check this value direction
                if (first):
                        first = False
                        recordTime = currTime
                else:
                        dt = currTime - lastTime
                        DError = Kd * ((sensorError - lastError) / dt)
                        IError = IError + Ki * sensorError * dt
                PError = Kp * sensorError

                if (currTime - recordTime > 0.05):
                        recordTime = currTime
                        errorData.append((currTime, sensorError, PError, DError, IError))

                motorController = PError + DError + IError
                robot.drive_robot_power(motorController, motorController)
                lastTime = currTime
                lastError = sensorError
                time.sleep(0.01)

if __name__ == '__main__':
        main()
