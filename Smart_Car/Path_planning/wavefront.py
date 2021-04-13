import numpy as np
import transforms as tf
import math
import copy
import gridmap as gd

def get_8_neighbors(grid, x, y):
        ylen = len(grid)
        xlen = len(grid[0])
        neighbors = []
        if (x >= xlen or y >= ylen):
                return []
        if (x > 0):
                if (y > 0):
                        neighbors.append([x-1, y-1])
                if (y < ylen - 1):
                        neighbors.append([x-1, y+1])
                neighbors.append([x-1, y])

        if (x < xlen - 1):
                if (y > 0):
                        neighbors.append([x+1, y-1])
                if (y < ylen - 1):
                        neighbors.append([x+1, y+1])
                neighbors.append([x+1, y])

        if (y > 0):
                neighbors.append([x, y-1])
        if (y < ylen - 1):
                neighbors.append([x, y+1])

        return neighbors

def get_4_neighbors(grid, x, y):
        ylen = len(grid)
        xlen = len(grid[0])
        neighbors = []

        if (x >= xlen or y >= ylen):
                return []
        if (y > 0):
                neighbors.append([x, y-1])
        if (x < xlen - 1):
                neighbors.append([x+1, y])
        if (y < ylen - 1):
                neighbors.append([x, y+1])
        if (x > 0):
                neighbors.append([x-1, y])
        
        return neighbors


def wave4(grid, x, y):
        queue = []
        queue.append([x, y])
        count = 1
        grid[y][x] = count
        while (len(queue) > 0):
                node = queue.pop(0)
                # print(node)
                # print(queue)
                # print(grid)
                xInd = node[0]
                yInd = node[1]
                neighbors = get_4_neighbors(grid, xInd, yInd)
                # print(neighbors)
                for neighbor in neighbors:
                        xN = neighbor[0]
                        yN = neighbor[1]
                        # print(neighbor)
                        if (grid[yN][xN] == 0):
                                # print('yeet')
                                # print(neighbor)
                                queue.append(neighbor)
                                grid[yN][xN] = grid[yInd][xInd] + 1
                                # print(grid)
        return grid

def wave8(grid, x, y):
        queue = []
        queue.append([x, y])
        count = 1
        grid[y][x] = count
        while (len(queue) > 0):
                node = queue.pop(0)
                # print(node)
                # print(queue)
                # print(grid)
                xInd = node[0]
                yInd = node[1]
                neighbors = get_8_neighbors(grid, xInd, yInd)
                # print(neighbors)
                for neighbor in neighbors:
                        xN = neighbor[0]
                        yN = neighbor[1]
                        # print(neighbor)
                        if (grid[yN][xN] == 0):
                                # print('yeet')
                                # print(neighbor)
                                queue.append(neighbor)
                                grid[yN][xN] = grid[yInd][xInd] + 1
                                # print(grid)
        return grid

def make_random_grid(xsize, ysize, obs_prob):
        grid = np.random.choice(np.arange(-1, 1), size=(ysize, xsize), p=[obs_prob, 1-obs_prob])
        return grid


def pretty_print(grid, finame):
        with open(finame, 'w') as fi:
                # f_string = '%s ' * (len(grid))

                for row in grid:
                        joinrows = ' '.join(str(x).rjust(3) for x in row)
                        # writeString = joinrows.rjust(12)
                        fi.write(joinrows) #writeString)
                        fi.write('\n')


def test_grid(four):
        xsize = 5
        ysize = 5
        startx = 3
        starty = 1
        obs_prob = 0.3
        grid = make_random_grid(xsize, ysize, obs_prob)
        if (not four):
                wvgrid = wave8(grid, startx, starty)
        else:
                wvgrid = wave4(grid, startx, starty)
        pretty_print(wvgrid, 'grid.txt')
        return wvgrid


def find_path_4_recurse(grid, startx, starty, path, last_count):
        squareOne = grid[starty][startx]
        if (squareOne <= 0 or squareOne >= last_count):
                return None
        elif (squareOne == 1):
                return 1
        else:
                neighbors = get_4_neighbors(grid, startx, starty)
                for neighbor in neighbors:
                        # print('ss', startx, starty)
                        # print(neighbor)
                        sol = find_path_4_recurse(grid, neighbor[0], neighbor[1], path, squareOne)
                        # print(sol)
                        if (sol is not None):
                                path.append(neighbor)
                                return path
                return None

def find_path_8_recurse(grid, startx, starty, path, last_count):
        squareOne = grid[starty][startx]
        if (squareOne <= 0 or squareOne >= last_count):
                return None
        elif (squareOne == 1):
                return 1
        else:
                neighbors = get_8_neighbors(grid, startx, starty)
                for neighbor in neighbors:
                        # print('ss', startx, starty)
                        # print(neighbor)
                        sol = find_path_8_recurse(grid, neighbor[0], neighbor[1], path, squareOne)
                        # print(sol)
                        if (sol is not None):
                                path.append(neighbor)
                                return path
                return None


def find_path(grid, startx, starty, four=False):
        if grid[starty][startx] <= 0:
                return None
        if four:
                path = find_path_4_recurse(grid, startx, starty, [], grid[starty][startx] + 1)
        else:
                path = find_path_8_recurse(grid, startx, starty, [], grid[starty][startx] + 1)
        path.append([startx, starty])
        path.reverse()
        return path

def relative_translations(path, xi, yi):
        # assumes transforms are a rotation, then a translation
        pathRobotFrame = []
        tempPath = copy.deepcopy(path)
        
        for j in range(len(tempPath) - 1):
                item = tempPath[j]
                nextItem = tempPath[j + 1]
                xj = item[0]
                yj = item[1]    
                xk = nextItem[0]
                yk = nextItem[1]
                

                transTgr = tf.invert_transform(tf.get_transform(xj, yj, 0))
                transTpg = tf.get_transform(xk, yk, 0)
                transTpr = tf.chain_transforms(transTgr, transTpg)
                transPpr = tf.get_pose_vec(transTpr)
                
                pathRobotFrame.append(transPpr)
        return pathRobotFrame

def match_angles(inList):
        if inList == [0, 1, 0]:
                return 0
        elif inList == [1, 1, 0]: 
                return -math.pi / 4
        elif inList == [1, 0, 0]: 
                return -math.pi/2
        elif inList == [1, -1, 0]: 
                return -3 * math.pi /4
        elif inList == [0, -1, 0]: 
                return math.pi 
        elif inList == [-1, -1, 0]: 
                return 3 * math.pi / 4
        elif inList == [-1, 0, 0]: 
                return math.pi / 2
        elif inList == [-1, 1, 0]: 
                return math.pi / 4

# def angleArith(ang1,ang2,sgn):
#         if (sgn > 0):
#                 theta = math.atan2(math.sin(ang1 + ang2), cos(ang1 + ang2))
#         else:
#                 theta = math.atan2(math.sin(ang2 - ang1), math.cos(ang2 - ang1))


#     theta = atan2(sin(ang1 + ang2), cos(ang1 + ang2));

        
#         else:
#         theta = atan2(sin(ang2 - ang1), cos(ang2 - ang1));
# return theta


def assign_angles(transpath):
        currAngle = 0
        nextAngle = 0
        first = True
        angList = []
        for i in range(len(transpath) - 1):
                x = 0
                y = 0
                if (first):
                        currAngle = match_angles(transpath[i])
                        Tgr = tf.get_transform(0, 0, currAngle)
                        first = False
                else:
                        Tgr = tf.invert_transform(tf.get_transform(0, 0, currAngle))
                nextAngle = match_angles(transpath[i+1])
                print(currAngle, nextAngle)
                
                Tpg = tf.get_transform(0, 0, nextAngle)
                Tpr = tf.chain_transforms(Tgr, Tpg)
                Ppr = tf.get_pose_vec(Tpr) 
                theta = Ppr[2]
                angList.append(theta)
                currAngle = nextAngle
        return angList

# def relative_rotations8(transpath):
#         rotpath = []
#         for i in range(len(transpath) - 1):
#                 point = transpath[i]
#                 nextPoint = transpath[i+1]
#                 if (point == [0, 1, 0]):
#                         if (nextPoint == [0, 1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [0, -1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(math.pi/2)
#                         elif (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(-math.pi/2)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(-3 * math.pi / 4)
#                         elif (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(math.pi / 4)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(-math.pi / 4)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#                 elif (point == [1, 1, 0]):
#                         if (nextPoint == [1, 1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [-1, -1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(-3 * math.pi/4)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(- math.pi / 2)
#                         elif (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(math.pi / 4)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(-3 * math.pi / 4)
#                 elif (point == [1, 0, 0]):
#                         if (nextPoint == [1, 0, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [-1, 0, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(-3 * math.pi/4)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(- math.pi / 2)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(math.pi / 4)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(-3 * math.pi / 4)
#                 elif (point == [1, -1, 0]):
#                         if (nextPoint == [1, -1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [-1, -1, 0]):
#                                 rotpath.append(-math.pi / 2)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(-math.pi/4)
#                         elif (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(- 3 * math.pi / 4)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#                 elif (point == [0, -1, 0]):
#                         if (nextPoint == [0, -1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [-1, 0, 0]):
#                                 rotpath.append(-math.pi / 2)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(-math.pi/4)
#                         elif (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(- 3 * math.pi / 4)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#                 elif (point == [-1, -1, 0]):
#                         if (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [-1, 1, 0]):
#                                 rotpath.append(-math.pi / 2)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(-math.pi/4)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(- 3 * math.pi / 4)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#                 elif (point == [-1, 0, 0]):
#                         if (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [0, 1, 0]):
#                                 rotpath.append(-math.pi / 2)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(-math.pi/4)
#                         elif (nextPoint == [1, 1, 0]):
#                                 rotpath.append(- 3 * math.pi / 4)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#                 elif (point == [-1, 1, 0]):
#                         if (nextPoint == [-1, 1, 0]):
#                                 rotpath.append(0)
#                         elif(nextPoint == [1, 1, 0]):
#                                 rotpath.append(-math.pi / 2)
#                         elif (nextPoint == [-1, 0, 0]):
#                                 rotpath.append(math.pi/4)
#                         elif (nextPoint == [0, 1, 0]):
#                                 rotpath.append(-math.pi/4)
#                         elif (nextPoint == [1, 0, 0]):
#                                 rotpath.append(- 3 * math.pi / 4)
#                         elif (nextPoint == [-1, -1, 0]):
#                                 rotpath.append(math.pi / 2)
#                         elif (nextPoint == [1, -1, 0]):
#                                 rotpath.append(math.pi)
#                         elif (nextPoint == [0, -1, 0]):
#                                 rotpath.append(3 * math.pi / 4)
#         rotpath.append(0)
#         for i in range(len(rotpath)):
#             rotpath[i] = -rotpath[i]

#         return rotpath


def relative_rotations(transpath):
        rotpath = []
        for i in range(len(transpath) - 1):
                x = transpath[i][0]
                y = transpath[i][1]
                nextX = transpath[i+1][0]
                nextY = transpath[i+1][1]
                if (x == -1):
                        if (nextX == -1):
                                rotpath.append(0)
                        elif (nextY == -1):
                                rotpath.append(math.pi/2)
                        else:
                                rotpath.append(-math.pi/2)
                elif (x == 1):
                        if (nextX == 1):
                                rotpath.append(0)
                        elif (nextY == -1):
                                rotpath.append(-math.pi/2)
                        else:
                                rotpath.append(math.pi/2)
                elif (y == -1):
                        if (nextY == -1):
                                rotpath.append(0)
                        elif (nextX == -1):
                                rotpath.append(-math.pi/2)
                        else:
                                rotpath.append(math.pi/2)
                elif (y == 1):
                        if (nextY == 1):
                                rotpath.append(0)
                        elif (nextX == -1):
                                rotpath.append(math.pi/2)
                        elif (nextX == 1):
                                rotpath.append(-math.pi/2)
                        else:
                                rotpath.append(math.pi)
        rotpath.append(0)
        return rotpath

def norm(vec):
        total = 0
        for item in vec:
                total = total + item**2
        return total

def to_distances8(transpath):
        distanceList = []
        for item in transpath:
                if (norm(item) == 2):
                        distanceList.append(2)
                else:
                        distanceList.append(norm(item))
        distanceList[0] = 0
        return distanceList

def to_ones(transpath):
        oneList = [1 for item in transpath]
        oneList[0] = 0
        return oneList

def combined_path8(path, xi, yi):
        transpath = relative_translations(path, xi, yi)
        print(transpath)
        transpath.insert(0, [0, 1, 0])
        rotpath = assign_angles(transpath)
        print(rotpath)
        onespath = to_distances8(transpath)
        finalRobotPath = zip(onespath, rotpath)
        return list(finalRobotPath)

def combined_path(path, xi, yi):
        transpath = relative_translations(path, xi, yi)
        print(transpath)
        transpath.insert(0, [0, 1, 0])
        rotpath = relative_rotations4(transpath)
        onespath = to_ones(transpath)
        finalRobotPath = zip(onespath, rotpath)
        return list(finalRobotPath)

def full_path_8point(xstart, ystart, xgoal, ygoal, testing=False, testGrid=None, convertInput=False):
        if (testing):
                grid = testGrid
        else:
                grid = gd.create_map()
        if (convertInput):
                xgoal = math.floor(xgoal/2)
                ygoal = math.floor(ygoal/2)
                xstart = math.floor(xstart/2)
                ystart = math.floor(ystart/2)
        print(grid)
        wv = wave8(grid, xgoal, ygoal)
        pretty_print(wv, 'grid.txt')
        init_path = find_path(wv, xstart, ystart, False)
        print(init_path)
        pretty_print_path(grid, init_path)
        return combined_path8(init_path, xstart, ystart)

def full_path_4point(xstart, ystart, xgoal, ygoal, testing=False, testGrid=None, convertInput=False):
        if (testing):
                grid = testGrid
        else:
                grid = gd.create_map()
        if (convertInput):
                xgoal = math.floor(xgoal/2)
                ygoal = math.floor(ygoal/2)
                xstart = math.floor(xstart/2)
                ystart = math.floor(ystart/2)
        print(grid)
        wv = wave4(grid, xgoal, ygoal)
        pretty_print(wv, 'grid.txt')
        init_path = find_path(wv, xstart, ystart, True)
        print(init_path)
        pretty_print_path(grid, init_path)
        return combined_path(init_path, xstart, ystart)


def pretty_print_path(grid, path):
        tempGrid = copy.deepcopy(grid)
        count = 0
        for waypoint in path:
                x = waypoint[0]
                y = waypoint[1]
                tempGrid[y][x] = 'p' + str(count)
                count = count + 1
        pretty_print(tempGrid, 'gridpath.txt')










