options = ['a1','f2','c3']
move = []
utility = [88,12,43]
for i in range(3):
    move.append([options[i],utility[i]])
sorted_option = sorted(move,key=lambda x:x[1])

print(sorted_option[0][0])


#color : 'W' 'B'
#you: 'BLACK'