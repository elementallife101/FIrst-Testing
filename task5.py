import numpy as np
import random
def binary_datastream(n):
    num = random.randint(0, (2**n)-1)
    binaryNum = np.binary_repr(num)
    while len(binaryNum) < n:
        binaryNum = "0" + binaryNum
    return binaryNum
print(binary_datastream(4))