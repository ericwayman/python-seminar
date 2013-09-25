import numpy
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches

class draw_rectangle:
    def __init__(self, ax_array,scatter_plots):
        self.click_loc = None
        self.ax_array = ax_array
        #initialize with an empty rectangle
        self.rect = matplotlib.patches.Rectangle((0,0),0,0,facecolor='orange') 
        #initialize the rectangle to be in the first axis.
        self.ax_array[0].add_patch(self.rect) 
        self.scatter_plots = scatter_plots
        self.data_pts = []
    #the function to connect all the events
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
            print event.inaxes
            print type(event.inaxes)
            print event.inaxes.get_geometry()
            num=event.inaxes.get_geometry()[2]
            #y_indx = num/4
            #x_indx = num - 4*(num/4)-1
            self.data_pts = self.scatter_plots[num].get_offsets()
        #otherwise don't do anything
        else: return
        #draw the rectangle
        self.rect.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will create a rectangle if a click is registered'
        #stops drawing the rectangle if the mouse hovers over points outside the current axis
        if event.inaxes != self.rect.axes: return
        #Don't do anything if not clicked on a point
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
        
        #find data points contained in the rectangle
        trutharray = self.rect.get_path().contains_points(self.data_pts)

        #draw the rectangle
        self.rect.figure.canvas.draw()
    
    def on_release(self, event):
        'on release we reset the press data'
        self.click_loc = None
        self.rect.figure.canvas.draw()
    
#make the grid of plots of the flower petal data
path = './hw_3_data'
fname = os.path.join(path, 'flowers.txt')
tab = np.loadtxt(fname,delimiter=',',skiprows=1,usecols=(0,1,2,3))
ncols=tab.shape[1]
gs = matplotlib.gridspec.GridSpec(ncols,ncols)
ax_array=[]
scat_array =[]
for i in range(0,ncols):
    for j in range(0,ncols):
        axis = plt.subplot(gs[i,j])
        scat=axis.scatter(tab[:,i],tab[:,j])
        ax_array.append(axis)
        scat_array.append(scat)    
dr = draw_rectangle(ax_array,scat_array)
dr.connect()
plt.show()




    