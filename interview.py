a = [1, 2, 3, 2, 2]

def duplicate(a):
    # {d:0 for d in a}
    d = dict.fromkeys(a, 0)


    for i in a:
        d[i] += 1

        if d[i] == 2:
            return(d)


print(duplicate(a))