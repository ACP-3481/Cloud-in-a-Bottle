import time

def size_calculator(n):
    n1 = n
    if n1 % 5 != 0:
        n1 = n1 + (5 - n1 % 5)
    n1 *= 1.6
    n1 += 33
    return int(n1)

count = 0
while True:
    size_calculator(count)
    
