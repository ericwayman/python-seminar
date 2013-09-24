import numpy
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches

class draw_rectangle:
    def __init__(self, ax_array):
        self.click_loc = None
        self.ax_array = ax_array
        #initialize with an empty rectangle
        self.rect = matplotlib.patches.Rectangle((0,0),0,0,facecolor='orange') 
        #initialize the rectangle to be in the first axis.
        self.ax_array[0].add_patch(self.rect) 
    def connect(self):
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
    
    def on_press(self, event):
        #if not scaling a current rectangle, record the click to make a new one
        if(self.click_loc == None):
            #on mouse click, delete the current rectangle and reinitialize the rectangle to the current patch
            self.rect.remove()
            self.rect = matplotlib.patches.Rectangle((0,0),0,0,facecolor='orange') 
            event.inaxes.add_patch(self.rect)
            self.click_loc = (event.xdata,event.ydata)
            print "rectangle created at (%f,%f)" %(self.click_loc[0],self.click_loc[1])
        #otherwise don't do anything
        else: return
        self.rect.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will create a rectangle if a click is registered'
        if event.inaxes != self.rect.axes: return
        if (self.click_loc is None): return
        x_0 = self.click_loc[0]
        y_0 = self.click_loc[1]
        	
        #set bottom left x coordinate and width of rectangle
        if event.xdata > x_0:
        	self.rect.set_x(x_0)
        	self.rect.set_width(event.xdata - x_0)
        else:
        	self.rect.set_x(event.xdata)	
        	self.rect.set_width(x_0 - event.xdata)
        
        #set bottom left y coordinate and height of rectangle
        if event.ydata > y_0:
        	self.rect.set_y(y_0)
        	self.rect.set_height(event.ydata - y_0)
        else:
        	self.rect.set_y(event.ydata)
        	self.rect.set_height(y_0-event.ydata)
        self.rect.figure.canvas.draw()
    
    def on_release(self, event):
        'on release we reset the press data'
        self.click_loc = None
        self.rect.figure.canvas.draw()
    
#make the grid of plots
path = './hw_3_data'
fname = os.path.join(path, 'flowers.txt')
tab = np.loadtxt(fname,delimiter=',',skiprows=1,usecols=(0,1,2,3))
fig = plt.figure()
ncols=tab.shape[1]
ax_array=[]
for i in range(0,ncols):
    for j in range(0,ncols):
        axis = fig.add_subplot(ncols,ncols,ncols*i+j+1)
        axis.scatter(tab[:,i],tab[:,j])
        ax_array.append(axis)    
dr = draw_rectangle(ax_array)
dr.connect()
plt.show()




    