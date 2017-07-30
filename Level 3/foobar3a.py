def answer(l):
    lon = len(l)
    i_divide = [0]*lon
    im_divided_by = [0]*lon

    for i in range(lon):
        count = 0
        for j in range(i+1, lon):
            if(l[j]%l[i] == 0):
                count += 1
                im_divided_by[j] += 1
        i_divide[i] = count

    return sum([a*b for a,b in zip(i_divide, im_divided_by)])
