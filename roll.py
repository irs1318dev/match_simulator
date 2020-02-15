import random 

min = 1
max = 6

def roll(_min, _max):
    return random.randint(_min, _max)

def sum_rolls(num):
    count =0
    for i in range (0, num):
        count += roll(min, max) 
    return count  

def compare_rolls(num, val):
    roll = sum_rolls(num)
    if (roll > val):
        return 1
    elif (roll < val):
        return -1
    else:
        return 0

def find_group(num, groups):
    group=0
    for i in groups:
        group = group + 1
        if num in i:
            return group 
    return -1    


