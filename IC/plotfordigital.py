import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure(figsize=(4.5,3.8), dpi=200)
plt.xlabel("Year wise")
plt.ylabel("In crores")
years = [str(year) for year in range(2014, 2019)]
visitors = (61,80.46,99.92,120,122.29)
index = np.arange(len(years))
bar_width = 0.5
plt.bar(index, visitors, bar_width,  color=["green","red","cyan","purple","blue"])
plt.xticks(index, years) # labels get centered
plt.show()



last_week_cups = (9.96, 0.01, 14.06, 4.21, 2.57)
this_week_cups = (36.84, 52.49, 39.34, 14.99, 13.71)
names = ['Mobile wallets', 'BHIM+UPI', 'Debit card', 'IMPS', 'Aadhar EPS']

fig = plt.figure(figsize=(5,4), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.35   
ticks = np.arange(len(names))    
ax.bar(ticks, last_week_cups, width, label='Oct 2016')
ax.bar(ticks + width, this_week_cups, width, align="center",
    label='Nov 2018')

ax.set_ylabel('In crores')
ax.set_title('Modes of transaction')
plt.xticks(rotation=90)
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)

ax.legend(loc='best')
plt.show()
