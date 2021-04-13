import simbot as sb
import time
import matplotlib.pyplot as plt
import math 

def fig8Vw(t):
	v = 0.2
	sf = 1
	ks = 1
	kth = 2 * math.pi 
	kk = 15.1084
	s = v * t
	k = (kk / ks) * math.sin(kth * s)
	w = v * k
	return [v, w]

def main():
	sBot = sb.SimBot(1, 1)
	dataX = []
	dataY = []
	dataTh = []
	rotSpeeds = [[45, 90]]
	leftEnc = 0
	rightEnc = 0
	for item in rotSpeeds:
		startTime = time.time()
		lastTime = 0
		currTime = 0
		first = True
		while (time.time() - startTime <= 5):
			currTime = time.time()
			if (first):
				first = False
			else:
				dt = currTime - lastTime
				myWvels = sBot.get_rotSpeed()
				leftEnc += (myWvels[0] * dt)
				rightEnc += (myWvels[1] * dt)
				sBot.update_odometry(leftEnc, rightEnc, dt)
				dat = sBot.get_odom()
				dataX.append(dat[0])
				dataY.append(dat[1])
				dataTh.append(dat[2])
			vals = fig8Vw(currTime)
			vels = sBot.ik(vals[0], vals[1])
			wvels = sBot.vlvrTowlwr(vels[0], vels[1])
			wvels = [wvels[0] * 180 / math.pi, wvels[1] * 180 / math.pi]
			sBot.drive_rotSpeed(wvels[0], wvels[1])
			lastTime = currTime
			time.sleep(0.05)
	# print(dataY, dataX)
	print(dataTh)
	plt.plot(dataX, dataY)
	plt.show()



if __name__ == '__main__':
	main()