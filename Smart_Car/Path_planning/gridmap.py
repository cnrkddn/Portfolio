

def create_map():
	row = 27 # outer loop, y
	col = 36 # inner loop, x

	m = []
	for i in range(row):
		m.append([])
		for j in range(col):
			m[i].append(0)


	# walls
	for i in range(row):
		for j in range(2):
			m[i][j] = -1
			m[i][col - j - 1] = -1		

	for i in range(2):
		for j in range(col):
			m[i][j] = -1
			m[row - i - 1][j] = -1

	# big block, left
	m[9][3] = -1
	m[16][3] = -1
	m[16][4] = -1
	m[11][5] = -1
	m[12][5] = -1
	m[12][6] = -1

	m[9][2] = -1
	m[9][3] = -1
	m[9][4] = -1
	m[10][5] = -1
	m[11][6] = -1
	m[12][7] = -1
	m[13][8] = -1
	m[14][9] = -1

	for i in range(15, 21):
		m[i][10] = -1

	for j in range(7, 10):
		m[19][j] = -1

	for i in range(10, 16):
		for j in range(2, 5):
			m[i][j] = -1

	for i in range(13, 18):
		for j in range(5, 8):
			m[i][j] = -1

	for i in range(14, 20):
		m[i][8] = -1
		if i == 0:
			continue
		m[i][9] = -1

	for j in range(6, 10):
		m[18][j] = -1
		if i == 0:
			continue
		m[19][j] = -1

	# small block, left

	m[10][9] = -1
	m[10][14] = -1
	m[10][8] = -1
	m[10][16] = -1
	m[9][9] = -1
	m[9][15] = -1
	m[11][9] = -1
	m[11][15] = -1
	m[10][15] = -1

	for i in range(8, 13):
		for j in range(10, 15):
			m[i][j] = -1

	m[7][12] = -1
	m[13][12] = -1
	m[7][11] = -1
	m[7][13] = -1
	m[6][12] = -1
	m[13][11] = -1
	m[13][13] = -1
	m[14][12] = -1
	for j in range(11, 14):
		m[8][j] = -1
		m[12][j] = -1

	# small block, right

	for i in range(17, 23):
		for j in range(25, 32):
			m[i][j] = -1

	m[17][24] = -1
	m[18][24] = -1
	m[16][25] = -1
	m[16][26] = -1

	# big block, right

	m[16][15] = -1
	m[17][15] = -1
	m[18][15] = -1
	m[17][14] = -1
	m[21][17] = -1
	m[21][16] = -1
	m[21][18] = -1
	m[15][15] = -1
	m[15][16] = -1
	m[14][17] = -1
	m[16][14] = -1
	m[18][14] = -1
	m[19][15] = -1
	m[14][15] = -1
	m[14][16] = -1
	m[15][14] = -1
	m[12][17] = -1
	m[11][18] = -1

	for i in range(16, 21):
		for j in range(16, 19):
			m[i][j] = -1

	m[13][18] = -1
	m[14][18] = -1
	m[15][18] = -1
	m[15][17] = -1
	m[19][19] = -1
	m[10][21] = -1
	m[10][20] = -1
	m[10][22] = -1
	m[12][18] = -1
	m[13][17] = -1
	m[13][16] = -1
	m[11][18] = -1

	for i in range(11, 19):
		for j in range(19, 22):
			m[i][j] = -1

	for i in range(11, 18):
		m[i][22] = -1

	m[13][24] = -1
	m[15][23] = -1

	for i in range(11, 15):
		m[i][23] = -1
		m[i][24] = -1




	print(m)

	return m

# create_map()
