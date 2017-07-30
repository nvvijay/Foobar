import itertools

def answer(num_buns, num_required):
    conf = [[] for x in range(num_buns)]
    num_required = num_buns+1 - num_required
    comb = list(itertools.combinations(range(num_buns), num_required))
    for i, val in enumerate(comb):
        for j in val:
            conf[j].append(i)
    return conf
