import sys
sys.path.append('../')
# import robot as rb
import time 
import signal 
import numpy as np
import matplotlib.pyplot as plt 
import math
import copy

size = 16
ang_list = np.array([math.pi/8 * i for i in range(size)])

# rel is mod pi/8
def last_two_prob(prob_map, ind, rel_theta):
	pCurr = prob_map[ind] * ((- 4.8 /  math.pi) * rel_theta + 0.7)
	pNext = prob_map[ind - 1] * ( 3.2/ math.pi * rel_theta + 0.1)
	return pCurr + pNext

def convert_angle(ang):
    return math.atan2(math.sin(ang), math.cos(ang))

def signal_handler(sig, frame):
    robot.stop()
    sys.exit(0)
# only generates forward half
def generate_gaussian_prob(mean, std, x):
	if (x > mean):
		return 0.001
	k = 1 / (math.sqrt((2 * math.pi * std**2)))
	ePart = np.exp((-(x - mean)**2) / (2 * std**2))
	return k * ePart

def normalize(prob_map):
    total = sum(prob_map)
    return [item / total for item in prob_map]

def update_transition_last_two(prob_map, rel_theta, started=True):
    # odom theta should be mod 2 * pi
    if (not started):
        return []
    new_prob_map = np.zeros(len(prob_map))
    # print(prob_map)
    for i in range(len(prob_map)):
        # shift the mean by odom_theta
        new_prob_map[i] = last_two_prob(prob_map, i, rel_theta)
    # real_prob_map = [sum(item) for item in new_prob_map]
    # print(real_prob_map)
    return normalize(new_prob_map)

def update_transition_probabilities(prob_map, odom_theta, started=True):
    # odom theta should be mod 2 * pi
    if (not started):
        return []
    new_prob_map = []
    std = 0.2
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

def update_observation_probabilities(prob_map, obs, bitVec, zeroIndices, oneIndices, started=True):
    new_prob_map = copy.deepcopy(prob_map)
    prob_vec = np.zeros(len(prob_map))
    if (not started):
    	return []
    if (not obs):
        prob_vec[zeroIndices] = 0.95
        prob_vec[oneIndices] = 0.05
    else:
        prob_vec[zeroIndices] = 0.1
        prob_vec[oneIndices] = 0.9
    new_prob_map = np.multiply(new_prob_map, prob_vec)
    return normalize(new_prob_map) 

def getBitVec(vecsize):
	obs_prob = 0.6
	grid = np.random.choice(np.arange(0, 2), size=(vecsize), p=[obs_prob, 1-obs_prob])
	print(grid)
	return grid

def rotateBitVec(bitVec, start):
	return bitVec[start:] + bitVec[:start]

def main():
	# ang_list = np.array([math.pi/8 * i for i in range(16)])
	bitVec = getBitVec(size)
	prob_map = np.array([1/size for i in range(size)])
	zeroIndices = np.where(bitVec == 0)
	oneIndices = np.where(bitVec == 1)
	oneAngles = ang_list[oneIndices]
	startTime = time.time()
	confidenceThreshold = 0.5
	currTime = startTime
	dtheta = math.pi/20 - 0.001
	totalTheta = math.pi
	goal = 2
	time.sleep(0.1)
	plt.plot(prob_map)
	plt.show()
	totalT = 0
	first = True
	while(currTime - startTime < 80):
		currTime = time.time() 
		
		obs = 0
		for oneAng in oneAngles:
			if (math.sqrt((oneAng - totalTheta)**2) <= math.pi/16):
				obs = 1

		new_p_map = update_observation_probabilities(prob_map, obs, bitVec, zeroIndices, oneIndices)
		# print('new_p_map:', new_p_map)
		totalTheta = (totalTheta + dtheta) % (math.pi/8 * size)
		totalT = totalT + dtheta
		relTheta = totalTheta % (math.pi / 8)
		final_p_map = update_transition_last_two(new_p_map, relTheta)
		# final_p_map = update_transition_probabilities(new_p_map, relTheta)
		# print('final_p_map:', final_p_map)
		plt.cla()
		plt.plot(final_p_map)
		plt.pause(0.01)
		print('Obs:', obs)
		print('GOal:', final_p_map[goal])
		if (final_p_map[goal] >= confidenceThreshold):
			print('yay')
			break
		time.sleep(0.4)
		print('Theta:', totalTheta)
		print('RelTheta:', relTheta)
		relTheta = totalTheta % (math.pi / 8)
	
		prob_map = final_p_map
	print(totalT)
	plt.cla()
	plt.plot(final_p_map)
	plt.show()



if __name__ == '__main__':
	main()
