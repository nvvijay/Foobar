from fractions import Fraction
from functools import reduce
import operator

def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def get_iden_mat(len):
    out = []
    for i in range(len):
        inr = []
        for j in range(len):
            if(i == j):
                inr.append(Fraction(1,1))
            else:
                inr.append(Fraction(0,1))
        out.append(inr)
    return out

def transpose_mat(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def get_minor(m,i,j):
    return [r[:j] + r[j+1:] for r in (m[:i]+m[i+1:])]

def get_detmt(m):
    det = 0
    if(len(m) == 1):
        return m[0][0]
    if(len(m) == 2):
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    else:
        for i in range(len(m)):
            sign = (-1)**i
            det += (sign*m[0][i]*get_detmt(get_minor(m, 0, i)))
    return det

def invert_mat(m):
    det = get_detmt(m)
    #special case
    if len(m) == 1:
        return [[Fraction(1, det)]]
    if len(m) == 2:
        return [[m[1][1]/det, -1*m[0][1]/det],
                [-1*m[1][0]/det, m[0][0]/det]]

    c = []
    for i in range(len(m)):
        c_row = []
        for j in range(len(m)):
            mi = get_minor(m,i,j)
            c_row.append(((-1)**(i+j)) * get_detmt(mi))
        c.append(c_row)
    c = transpose_mat(c)
    for i in range(len(c)):
        for j in range(len(c)):
            c[i][j] = c[i][j]/det
    return c
    #newfound appreciation for numpy

def mod_mat_mul(l, m):
    prod = []
    for i in range(len(m[0])):
        col = [x[i] for x in m]
        prod.append(sum([x*y for x, y in zip(l, col)]))
    return prod

def preprocess(m):
    # if steady states are interspersed, need to move then over to the bottom
    sums = [sum(x) for x in m]
    top_ptr = 0
    btm_ptr = len(sums)-1
    swaps = []
    
    while(top_ptr < btm_ptr):
        while(sums[top_ptr] != 0):
            top_ptr += 1
        while(sums[btm_ptr] == 0):
            btm_ptr -= 1
        if(top_ptr < btm_ptr):
            swaps.append((top_ptr, btm_ptr))
            temp = sums[top_ptr]
            sums[top_ptr] = sums[btm_ptr]
            sums[btm_ptr] = temp
            top_ptr += 1
            btm_ptr -= 1

    for j, i in swaps:
        #swapping row i, j
        temp = m[i]
        m[i] = m[j]
        m[j] = temp

        #swapping column i, j
        for r in range(len(m)):
            temp = m[r][i]
            m[r][i] = m[r][j]
            m[r][j] = temp

    return m, swaps
    
def answer(m):
    # special case where the ore is apparently hydrogen, aarghhh
    if(len(m) == 1):
        return [1,1]

    m, swaps = preprocess(m)
    # terminal states
    t_rows = []
    
    # for denomenators
    row_sums = [0]*len(m)
    
    for i in range(len(m)):
        s = sum(m[i])
        
        # absorbing states
        if(s == 0):
            m[i][i] = 1
            s = 1
            t_rows.append(i)

        row_sums[i] = s

    # convert ints to fractions
    new_m = []
    for i in range(len(m)):
        row = []
        for j in range(len(m[i])):
            row_denom = row_sums[i]
            row.append(Fraction(m[i][j], row_denom))
        new_m.append(row)

    # convert to QR form
    m = []
    for i in reversed(t_rows):
        new_m.pop(i)
    for i in range(len(new_m)):
        m.append(new_m.pop(0))

    # orthogonal matrix
    orth_m = [m[i][:len(m)] for i in range(len(m))]
    #rectangular matrix
    rect_m = [m[i][len(m):] for i in range(len(m))]

    # finding I-Q inverse
    imq = list(map((lambda x, y: list(map(operator.sub, x, y))), get_iden_mat(len(orth_m)), orth_m))
    imqi = invert_mat(imq)
    
    probs = mod_mat_mul(imqi[0], rect_m)
    
    # find common denom
    denoms = []
    numers = []
    for i in range(len(probs)):
        denoms.append(probs[i].denominator)
        numers.append(probs[i].numerator)
    denom = reduce(lcm, denoms)

    op = []
    for i in range(len(numers)):
        mult = denom//denoms[i]
        op.append(numers[i]*mult)

    reorder = []
    if(len(swaps) > 0):
        #reshuffle output order like it was b4 reordering
        for j, i in swaps:
            pos = len(row_sums)-(i)
            reorder.append(op.pop(-pos))

    op = reorder+op
    op.append(denom)
    return op


m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [7, 6, 8, 21]")
m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [0, 3, 2, 9 ,14]")
m = [[1, 2, 3, 0, 0, 0], [4, 5, 6, 0, 0, 0], [7, 8, 9, 1, 0, 0], [0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [1, 2, 3]")
m = [[0]]
print("got :",answer(m))
print("exp : [1, 1]")
m = [[0, 0, 12, 0, 15, 0, 0, 0, 1, 8], [0, 0, 60, 0, 0, 7, 13, 0, 0, 0], [0, 15, 0, 8, 7, 0, 0, 1, 9, 0], [23, 0, 0, 0, 0, 1, 0, 0, 0, 0], [37, 35, 0, 0, 0, 0, 3, 21, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [1, 2, 3, 4, 5, 15]")
m = [[ 0,  7,  0, 17,  0,  1,  0,  5,  0,  2], [ 0,  0, 29,  0, 28,  0,  3,  0, 16,  0], [ 0,  3,  0,  0,  0,  1,  0,  0,  0,  0], [48,  0,  3,  0,  0,  0, 17,  0,  0,  0], [ 0,  6,  0,  0,  0,  1,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]
print("got :",answer(m))
print("exp : [4, 5, 5, 4, 2, 20]")
m = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [1, 1, 1, 1, 1, 5]")
m = [[1, 1, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [2, 1, 1, 1, 1, 6]")
m = [[0, 86, 61, 189, 0, 18, 12, 33, 66, 39], [0, 0, 2, 0, 0, 1, 0, 0, 0, 0], [15, 187, 0, 0, 18, 23, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [6, 44, 4, 11, 22, 13, 100]")
m = [[0, 0, 0, 0, 3, 5, 0, 0, 0, 2], [0, 0, 4, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0, 1, 1], [13, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 1, 8, 7, 0, 0, 0, 1, 3, 0], [1, 7, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
print("got :",answer(m))
print("exp : [1, 1, 1, 2, 5]")

m = [[0,10,1,1],[0,0,0,0],[0,1,0,0],[0,0,0,0]]
print(answer(m))
