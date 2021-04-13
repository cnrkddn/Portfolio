#!/usr/bin/env python3

import robot as rob
import time 

def main():
        robot = rob.Robot()
        print("BAttery:" + str(robot.get_robot_battery()))
        robot.stop()
        powPairs = [[30, 20], [20, 30], [-30, 0]]
        for index in range(len(powPairs)):
                powers = powPairs[index]
                startTime = time.time()
                lastTime = startTime
                currTime = lastTime
                    # if (dtime < 1 and dtime is not 0):
                      #   robot.drive_robot_power(powers[0] * dtime, powers[1] * dtime)
                    # elif (dtime > 2):
                    #     robot.drive_robot_power(powers[0] * (3 - dtime), powers[1] * (3- dtime))
                    # else:
                left_scale = 1
                right_scale = 1
                if index == 2:
                    right_scale = 1
                robot.drive_robot_power(left_scale * powers[0], right_scale * powers[1])
 
                first = True
                dtime = 0
                while(currTime - startTime  < 3):
                    if (first):
                        first = False
                    else:
                        currTime = time.time()
                        dtime = currTime - lastTime
                        robot.update_robot_odometry(dtime)
                        lastTime = currTime
                        # print(dtime)
                    # might cause some issues in the near future, will see
                    
                    time.sleep(0.01)
                    

                robot.stop()
                time.sleep(3)

        print("x, y: ", end=' ')
        print((robot.get_robot_odometry())[:-1]) 
        robot.stop()

if __name__ == '__main__':
        main()



