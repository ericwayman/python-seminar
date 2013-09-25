import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import os

#define data
dt = [("frac_followed",np.float32),("frac_observed",np.float32),
("frac_observed_uncertainty",np.float32)]
path='./HW31_example'

#define file names 
eff_fname = os.path.join(path,'Efficiency.txt')
pur_fname = os.path.join(path,'Purity.txt')



#load data
tab_eff= np.loadtxt(eff_fname, dtype = dt,skiprows=1)
tab_pur = np.loadtxt(pur_fname, dtype = dt,skiprows=2)



#creat new figure and plot
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

#set axis limits
ax1.set_xlim(-0.1, 1.1)
ax2.set_xlim(-0.1, 1.1)
ax1.set_ylim(-0.1, 1.1)
ax1.set_ylim(-0.1, 1.1)


#plot the data lines
eff_line=ax1.plot(tab_eff['frac_followed'],tab_eff['frac_observed'],
	linewidth=2,color='black')
eff_line_plus_uncert=ax1.plot(tab_eff['frac_followed'],
	tab_eff['frac_observed']+tab_eff['frac_observed_uncertainty'],
	linewidth=2,color='black')
eff_line_minus_uncert=ax1.plot(tab_eff['frac_followed'],
	tab_eff['frac_observed']-tab_eff['frac_observed_uncertainty'],
	linewidth=2,color='black')

pur_line=ax2.plot(tab_pur['frac_followed'],tab_pur['frac_observed'],
	linewidth=2,color='black')
pur_line_plus_uncert=ax2.plot(tab_pur['frac_followed'],
	tab_pur['frac_observed']+tab_pur['frac_observed_uncertainty'],
	linewidth=2,color='black')
pur_line_minus_uncert=ax2.plot(tab_pur['frac_followed'],
	tab_pur['frac_observed']-tab_pur['frac_observed_uncertainty'],
	linewidth=2,color='black')

#fill region inbetween lines with grey
ax1.fill_between(tab_eff['frac_followed'],
	tab_eff['frac_observed']-tab_eff['frac_observed_uncertainty'],
	tab_eff['frac_observed']+tab_eff['frac_observed_uncertainty'], facecolor='grey', alpha=0.25)
ax2.fill_between(tab_pur['frac_followed'],
	tab_pur['frac_observed']-tab_pur['frac_observed_uncertainty'],
	tab_pur['frac_observed']+tab_pur['frac_observed_uncertainty'], facecolor='grey', alpha=0.25)

#make straight lines
x = np.linspace(0, 1.0)
y = (18.0/135.0) + 0*x
y2=np.arange(0,0.4,.02)
x2 = .2 + 0*y2
ax1.plot(x,x,linewidth=2,color='black')
ax2.plot(x,y,linewidth=2,color='black')
ax2.plot (x2,y2,'o',color='black',linewidth=.5)
#make titles
ax1.set_title('Efficiency',fontsize=20,fontweight='bold')
ax2.set_title('Purity',fontsize=20,fontweight='bold')

#label axes
ax1.set_xlabel('Fraction of GRBs Followed Up')
ax1.set_ylabel('Fraction of high (z>4) GRBs observed')
ax2.set_xlabel('Fraction of GRBs Followed Up')
ax2.set_ylabel('Percent of observed GRBS that are high z (z>4)')

#make ticks
ax1.tick_params(which='major',length =3,width =1,top='off',right='off')
ax2.tick_params(which='major',length =3,width =1,top='off')
ax2.tick_params(which='major',direction='out',axis='y',labelright='on')

#add annotations
ax1.annotate("Follow up 20% of \n bursts to capture ~55% \n of high-z events" , 
	xy=(.2, .6), xytext=(.35, .15),
            arrowprops=dict(facecolor='black', width=0.8, headwidth=7, shrink=0.08))
ax1.annotate("Random \n guessing" , 
	xy=(.82, .8), xytext=(.82, .4),
            arrowprops=dict(facecolor='black', width=0.8, headwidth=7, shrink=0.08))
ax2.annotate("Random \n guessing" , 
	xy=(.6,.12), xytext=(.62, .5),
            arrowprops=dict(facecolor='black', width=0.8, headwidth=7, shrink=0.08))
ax2.annotate("If 20% of evens are \n followed up, ~40% \n of them will be high-z" , 
	xy=(.2,.35), xytext=(.2, .8),
            arrowprops=dict(facecolor='black', width=0.8, headwidth=7, shrink=0.08))


plt.show()
plt.savefig('hw_3_1_plot.png')
