T = int(input())
for j in range(T):
    inps = input()
    data = inps.split()
    x,y = map(int,data)
    a=0
    b=0
    for i in range(11):
        strt = 10*(i-1)+1
        stop = 10*i
        if x >= strt and x <= stop:
            a = i
        if y >= strt and y<= stop:
            b = i
    if a > b:
        print(a-b)
    else:
        print(b-a)