def compositions(t=2, s=2):
    q = [0] * (t + 1)
    r = None
    q[0] = s
    while True:
        yield q
        if q[0] == 0:
            if r == t:
                break
            else:
                q[0] = q[r] - 1
                q[r] = 0
                r = r + 1
        else:
            q[0] = q[0] - 1
            r = 1
        q[r] = q[r] + 1


def compositions2(t, s, q=[0, 0, 0], i=0):
    if i == t:
        q[i] = s
        yield q
    else:
        for x in range(s, -1, -1):
            # print i, x
            q[i] = x
            for y in compositions2(t, s - x, q, i + 1):
                yield y


for x in compositions(2, 5):
    print(x)
