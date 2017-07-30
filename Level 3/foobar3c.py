import math

memory = [[-1 for x in range(201)] for y in range(201)]
    
def get_config_count(num_bricks, curr_ht):
    brick_left = num_bricks - curr_ht
    #terminal case
    if(brick_left == 0 or curr_ht == 1):
        return 0
    #memoization
    if(memory[brick_left][curr_ht] != -1):
        return memory[brick_left][curr_ht]

    conf_count = 0
    #terminating state
    if(curr_ht > brick_left):
        conf_count += 1

    #recursion
    max_ht = brick_left -1
    min_ht = int(math.sqrt(2*brick_left))
    for ht in range(min_ht, max_ht+1):
        if(ht >= curr_ht):
            break
        conf_count += get_config_count(brick_left, ht)

    memory[brick_left][curr_ht] = conf_count
    return conf_count

def answer(n):
    num_bricks = n
    total = 0
    #max height in case of 2 steps only
    max_ht_pos = n-1
    #min height if numbers are consecutive
    min_ht_pos = int(math.sqrt(2*n))

    for ht in range(min_ht_pos, max_ht_pos+1):
        total += get_config_count(num_bricks, ht)

    return total

print(answer(200))
