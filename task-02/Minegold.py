T = int(input())
for i in range(T):
    inps = input()
    data = inps.split()
    N,X,Y = map(int,data)
    if (N+1)*Y>=X:
        print('YES')
    else:
        print('NO')