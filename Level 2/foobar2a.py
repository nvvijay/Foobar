def answer(l, t):
    start = 0
    sum_so_far = l[0]
    for i in range(1,len(l)+1):
        while(sum_so_far > t and start < i-1):
            sum_so_far = sum_so_far - l[start]
            start = start+1

        if(sum_so_far == t):
            return [start, i-1]

        if(i < len(l)):
            sum_so_far = sum_so_far + l[i]

    if(sum_so_far == t):
        return [start, len(l)]
        
    return [-1, -1]

l = [1,2,3,4]
t = 10
print(answer(l, t))
t = 15
print(answer(l, t))

l = [15]
t = 15
print(answer(l, t))

l=[16]
print(answer(l, t))

l = [15, 15, 16]
print(answer(l, t))

l = [16,15]
print(answer(l, t))

l = [4,3, 5, 7, 8]
t = 12
print(answer(l, t))

