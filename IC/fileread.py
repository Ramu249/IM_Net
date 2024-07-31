import csv
with open("C:\Users\hp\Downloads\latex pictures\influence-maximization-master\graphdata\arxiv1.txt",'r') as f:
    # Printing Specific Part of CSV_file
    # Printing last line of second column
    lines = list(csv.reader(f, delimiter = ' ', skipinitialspace = True))
    print(lines[-1][1])
    # For printing a range of rows except 10 last rows of second column
    for i in range(len(lines)-10):
        print(lines[i][1])
