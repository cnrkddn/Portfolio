import numpy as np
import math
def get_transform(x, y, th):
    return np.array([[math.cos(th), -math.sin(th), x],
                     [math.sin(th), math.cos(th), y],
                     [0, 0, 1]])

def invert_transform(mat):
    return np.linalg.inv(mat)

def chain_transforms(mat1, mat2):
    return np.matmul(mat1, mat2)

def get_pose_vec(mat):
    x = mat[0][2]
    y = mat[1][2]
    th = math.atan2(-mat[0][1], mat[0][0])
    return [x, y, th]