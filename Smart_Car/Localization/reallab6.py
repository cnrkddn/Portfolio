import sys
sys.path.append('../')
import robot as rb
import time 
import signal 
# import numpy as np
# import matplotlib.pyplot as plt 
import math
import copy

size = 16
robot = rb.Robot(wheelbase=7.25, radius=1.625)
# ang_list = np.array([math.pi/8 * i for i in range(size)])

# rel is mod pi/8
def last_two_prob(prob_map, ind, rel_theta):
        pCurr = prob_map[ind] * ((- 4.8 /  math.pi) * rel_theta + 0.85)
        pNext = prob_map[ind - 1] * (4.8 / math.pi * rel_theta + 0.15)
        return pCurr + pNext

def convert_angle(ang):
    return math.atan2(math.sin(ang), math.cos(ang))

def signal_handler(sig, frame):
    robot.stop()
    sys.exit(0)

# only generates forward half
# def generate_gaussian_prob(mean, std, x):
#       if (x > mean):
#               return 0.001
#       k = 1 / (math.sqrt((2 * math.pi * std**2)))
#       ePart = np.exp((-(x - mean)**2) / (2 * std**2))
#       return k * ePart

def normalize(prob_map):
    total = sum(prob_map)
    return [item / total for item in prob_map]

def update_transition_last_two(prob_map, rel_theta, started=True):
    # odom theta should be mod 2 * pi
    if (not started):
        return []
    new_prob_map = [0 for i in range(len(prob_map))]

    for i in range(len(prob_map)):
        new_prob_map[i] = last_two_prob(prob_map, i, rel_theta)

    return normalize(new_prob_map)

# def update_transition_probabilities(prob_map, odom_theta, started=True):
#     # odom theta should be mod 2 * pi
#     if (not started):
#         return []
#     new_prob_map = []
#     std = 0.2
#     for i in range(len(prob_map)):
#         # shift the mean by odom_theta
#         gaussian_mean = convert_angle(ang_list[i] - odom_theta)
#         # print(gaussian_mean)
#         temp_map = np.zeros(len(prob_map))
#         for j in range(len(prob_map)):
#             proper_angle = convert_angle(ang_list[j])
#             # print(proper_angle)
#             temp_map[j] = prob_map[j] * generate_gaussian_prob(gaussian_mean, std, proper_angle)
#         # print(temp_map)
#         new_prob_map.append(sum(temp_map))
#     # real_prob_map = [sum(item) for item in new_prob_map]
#     # print(real_prob_map)
#     return normalize(new_prob_map)

def update_observation_probabilities(prob_map, obs, bitVec, zeroIndices, oneIndices, started=True):
    new_prob_map = copy.deepcopy(prob_map)
    # prob_vec = [0 for i in range(len(prob_map))]
    if (not started):
        return []
    if (not obs):
        for i in range(len(prob_map)):
                if (i in zeroIndices):
                        new_prob_map[i] = prob_map[i] * 0.75
                else:
                        new_prob_map[i] = prob_map[i] * 0.25
    else:
        for i in range(len(prob_map)):
                if (i in oneIndices):
                        new_prob_map[i] = prob_map[i] * 0.75
                else:
                        new_prob_map[i] = prob_map[i] * 0.25
    return normalize(new_prob_map) 

# def getBitVec(vecsize):
#       obs_prob = 0.6
#       grid = np.random.choice(np.arange(0, 2), size=(vecsize), p=[obs_prob, 1-obs_prob])
#       print(grid)
#       return grid

# def rotateBitVec(bitVec, start):
#       return bitVec[start:] + bitVec[:start]

def get_obs():
        return robot.get_sensor(1) <= 30


def mainloop(bitVec, goal):
        # ang_list = np.array([math.pi/8 * i for i in range(16)])
        robot.set_sensor(2, 'light')
        robot.set_sensor(1, 'ultrasonic')
        prob_map = [1/size for i in range(size)]
        zeroIndices = [i for i in range(len(bitVec)) if bitVec[i] == 0]
        oneIndices = [i for i in range(len(bitVec)) if bitVec[i] == 1]

        confidenceThreshold = 0.26
        totalTheta = 0
        kp = 0.1
        baseSpeed = [20, 20]

        time.sleep(1)
        # plt.plot(prob_map)
        # plt.show()
        totalT = 0
        first = True

        startTime = time.time()
        currTime = startTime
        nowTime = 0
        lastTheta = 0
        currTheta = 0
        baseLight = 2300
        maxGoal = -1

        while(currTime - startTime < 80):
            currTime = time.time() 
            if (first):
                first = False
            else:
                dt = currTime - nowTime
                robot.update_odometry(dt) 
                currTheta = robot.get_odometry()[2]
                dtheta = currTheta - lastTheta
                # print('Time %.3f' % (currTime - startTime))
            # print('Odom', robot.get_odometry())
            # print('Displacement of L, R', robot.get_wheel_displacement())
            # print('Enc Readgins', robot.get_encoder_readings())
                lightSensed = robot.get_sensor(2)
                err = (lightSensed - baseLight)
                pControl = err * kp
                newPowLeft = baseSpeed[0] + (pControl)
                newPowRight = baseSpeed[1] - (pControl)
                robot.drive_robot_power(newPowLeft, newPowRight)
                if (dtheta <= math.pi/16):
                    time.sleep(0.05)
                    continue


                obs = get_obs()
                new_p_map = update_observation_probabilities(prob_map, obs, bitVec, zeroIndices, oneIndices)
                        # print('new_p_map:', new_p_map)
                totalTheta = (totalTheta + dtheta) % (math.pi/8 * size)
                totalT = totalT + dtheta
                relTheta = totalTheta % (math.pi / 8)
                final_p_map = update_transition_last_two(new_p_map, relTheta)
                        # final_p_map = update_transition_probabilities(new_p_map, relTheta)
                print('final_p_map:', final_p_map)
                # plt.cla()
                # plt.plot(final_p_map)
                # plt.pause(0.05)
                print('Obs:', obs)
                print('Goal:', final_p_map[goal])
                if (final_p_map[goal] >= confidenceThreshold or (final_p_map[goal] > maxGoal and currTime - startTime >= 50)):
                    print('yay')
                    break
                print('Theta:', totalTheta)
                print('RelTheta:', relTheta)
                prob_map = final_p_map
                nowTime = currTime
                lastTheta = currTheta
                if (final_p_map[goal] > maxGoal and currTime - startTime > 30):
                    maxGoal = final_p_map[goal]
 
            time.sleep(0.05)

        print(totalT)
        time.sleep(1.0)
        robot.stop()
        robot.BP.reset_all()
 
        # plt.cla()
        # plt.plot(final_p_map)
        # plt.show()


def main():
    pmap = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
    signal.signal(signal.SIGINT, signal_handler)
    goal = 1
    mainloop(pmap, goal)

if __name__ == '__main__':
    main()
    

