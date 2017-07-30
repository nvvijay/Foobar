def get_parent(node, root):
    ptr = root
    idx  = root

    while(ptr > 0):
        leftidx = idx - (ptr+1)/2
        rightidx = idx -1

        if(node == leftidx or node == rightidx):
            return idx;

        if(node<leftidx):
            idx = leftidx
        else:
            idx = rightidx
        ptr = int((ptr-1)/2)

    return -1;

def answer(h, l):
    root = (2**h) -1
    ans = []
    for i, val in enumerate(l):
        ans.append(int(get_parent(val, root)))

    return ans


h = 3
l = [1, 4, 7]
print(answer(h, l))

h = 3
l = [7,3,5,1]
print(answer(h, l))

h = 5
l = [19, 14, 28]
print(answer(h, l))
