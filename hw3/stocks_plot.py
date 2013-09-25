import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import os

#set data frame
dt = [('Date',int),('StockVal',np.float32)]
dt2 = [('Date',int),('Max_temp',int)]
path='./hw_3_data'

#define file names 
yahoo_fname = os.path.join(path,'yahoo_data.txt')
google_fname = os.path.join(path,'google_data.txt')
nytemp_fname = os.path.join(path,'ny_temps.txt')

#load data
tab_yahoo = np.loadtxt(yahoo_fname, dtype = dt,skiprows=1)
tab_google = np.loadtxt(google_fname, dtype = dt,skiprows=1)
tab_nytemp = np.loadtxt(nytemp_fname,dtype = dt2,skiprows=1)

#creat new figure and plot
fig=plt.figure()
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

#plot the data
lns1=ax.plot(tab_yahoo['Date'],tab_yahoo['StockVal'], label = 'Yahoo! Stock Value', linewidth=2, color='purple')
lns2= ax.plot(tab_google['Date'],tab_google['StockVal'], label = 'Google Stock Value', linewidth=2, color='b')
lns3= ax2.plot(tab_nytemp['Date'],tab_nytemp['Max_temp'],label= 'NY Mon. High Temp', linewidth=2, color='r',linestyle='--')

#make title
ax.set_title('New York Temperature, Google, and Yahoo!',fontsize=20)

#label axes
ax.set_xlabel('Date (MJD)')
ax.yaxis.set_label_position("left")
ax.set_ylabel('Value (Dollars)')
ax2.yaxis.set_label_position("right")
ax2.set_ylabel('Temperature (F)')
#set axis limits
ax.set_ylim([-20,780])
ax2.set_ylim([-150,100])
ax.set_xlim([48800,55600])

#add ticks
ax.minorticks_on()
ax2.minorticks_on()
ax.tick_params(which='major',length =5,width =2,top='off')
ax2.tick_params(which='major',length =5,width =2,top='off')
ax.tick_params(which='minor',length =3,width =1,top='off')
ax2.tick_params(which='minor',length =3,width =1,top='off')

#making the legend
lns = lns1+lns2+lns3
labels = [l.get_label() for l in lns]
leg = ax.legend(lns, labels,loc=6, prop={'size':10})
leg._drawFrame=False 

#show the plot
plt.show()

#save the plot
plt.savefig('hw_3_2_plot.png')
