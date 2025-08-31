T = int(input())
for i in range(T):
    inps = input()
    data = inps.split()
    X,Y = map(int,data)
    if Y <= X:
        print(Y)
    else:
        print(X)