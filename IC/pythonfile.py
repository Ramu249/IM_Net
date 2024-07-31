coloumn2 = []
with open(r'C:\Users\hp\Downloads\latex pictures\influence-maximization-master\graphdata\musgen3.txt') as f:
    data = f.readlines()
    #print(data)
    for line in data:
        data.append(line.split(" ")[1])
        print(
        
#list=[1,2,3,4,5]
#print(list)
with open('you.txt', 'w') as f:
    for item in data:
        f.write("%s\n" % item)
