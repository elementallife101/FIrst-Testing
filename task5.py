import numpy as np
import random
def binary_datastream(n):
    num = random.randint(0, (2**n)-1)
    binaryNum = np.binary_repr(num)
    while len(binaryNum) < n:
        binaryNum = "0" + binaryNum
    return binaryNum

def data_corruption(datastream):
    bit = random.randint(0, len(datastream) - 1)
    if datastream[bit] == 0:
        datastream[bit] = 1
    else:
        datastream[bit] = 0
    return datastream