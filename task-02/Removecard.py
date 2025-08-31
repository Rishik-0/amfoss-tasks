T = int(input())
for t in range(T):
    N = int(input())
    data = list(map(int,input().split()))       
    i=0
    ch = 0
    
    while i < len(data):
        cnt = data.count(data[i])
        i+=1

        if cnt>ch:
            ch = cnt
        
    print(len(data)-ch)