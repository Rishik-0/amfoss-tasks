T = int(input())
for i in range(T):
    flag = False
    count = 0
    i=0

    n,x = map(int,input().split(" "))
    data = list(map(int,input().split()))

    while i < len(data):
        if data[i]==1 and flag == False:
            flag = True          
            i+=x
        elif data[i]==0:
            i+=1
        elif flag == True and data[i]==1:
            print('NO')
            count = 1
            break

    if count == 0:
        print('YES')
                