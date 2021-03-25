a = [1,5,6,7,8,10,32,65,45]
sum = 0
for i in range(9):
    sum+=1 if a[i] > 10 else 0

print(sum)