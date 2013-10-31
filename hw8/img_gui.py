#Creates a GUI to to allow for an image search via google images
#The gui also features 3 buttons for image manipulation
#An image can be rotated 90 degrees clockwise, flipped about the yaxis or made into a gray scale

#query url  http://images.google.com/search?tbm=isch&q="your+query"
#imports
import matplotlib, sys, urllib2, simplejson
import matplotlib.image as mpimg
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from scipy import ndimage
from matplotlib import pylab as plt
import numpy as np
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

#def destroy(e): sys.exit()


root = Tk.Tk()
root.wm_title("Image search via google")
#root.bind("<Destroy>", destroy)


#intialze default image
root.image = mpimg.imread('default.jpg')
f = plt.figure()
#img = plt.imshow(root.image)
plt.imshow(root.image)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

#toolbar = NavigationToolbar2TkAgg( canvas, root )
#toolbar.update()
canvas._tkcanvas.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

#url_display shows the URL for the first image corresponding to the query
url_disp = Tk.StringVar()

#make widget functions

#conducts an image search of the query in searchbox.  Displays the first image found
def search():
	#extract the query from the searchbox
	search_term = searchbox.get()
	print "searched for: "+search_term
	
	search_term = search_term.replace(' ','%20')
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+search_term+'&userip=MyIP')

	request = urllib2.Request(url, None, {'Referer': search_term})
	response = urllib2.urlopen(request)
	
	# Process the JSON string.
	results = simplejson.load(response)
	data = results['responseData']
	img_url=data['results'][0]['unescapedUrl']
	
	#update the url in the url text box
	url_disp.set(img_url)
	
	#check and print the filename of the image
	file_name= img_url.split("/")[-1]
	print "the file name of the image is: " +file_name

	img_data = urllib2.urlopen(img_url).read()
	output = open('dl_img.jpg','wb')
	output.write(img_data)
	output.close()

	#update the displayed image to the image download
	root.image = mpimg.imread('dl_img.jpg')
	plt.imshow(root.image)
	canvas.show()
	root.update()

#reverses the image along the y axis
def img_reverse():
	original_image = root.image
	img_shape=original_image.shape
	if len(img_shape)==2:
		list_of_rows = list(original_image)
		list_of_rows_reversed = [row[::-1] for row in list_of_rows]
		reversed_array = np.asarray(list_of_rows_reversed)
		mirror = reversed_array.reshape(img_shape)
		root.image = mirror
		plt.imshow(root.image,cmap='gray')
		canvas.show()
		root.update()
	#compute mirror image for RGB channel images
	else:
		mirror = np.zeros(img_shape,dtype=np.uint8)
		for i in range(img_shape[2]):
			list_of_rows = list(original_image[:,:,i])
			list_of_rows_reversed = [row[::-1] for row in list_of_rows]
			reversed_array = np.asarray(list_of_rows_reversed)
			mirror[:,:,i] = reversed_array
		root.image = mirror
		plt.imshow(root.image)
		canvas.show()
		root.update()

#rotates an image 90 degrees clockwise
def img_rotate():
	original_image=root.image
	img_shape = original_image.shape
	if len(img_shape)==2:
		list_of_cols = list(original_image.transpose())
		list_of_cols_reversed = [col[::-1] for col in list_of_cols]
		img_rotated = np.asarray(list_of_cols_reversed)
		root.image = img_rotated
		plt.imshow(root.image,cmap='gray')
		canvas.show()
		root.update()
	else:
		img_rotated = np.zeros((img_shape[1],img_shape[0],3),dtype=np.uint8)
		for i in range(3):
			list_of_cols = list(original_image[:,:,i].transpose())
			list_of_cols_reversed = [col[::-1] for col in list_of_cols]
			img_rotated[:,:,i]=np.asarray(list_of_cols_reversed)
		root.image = img_rotated
		plt.imshow(root.image)
		canvas.show()
		root.update()

def img_grey():
	original_image=root.image
	img_shape = original_image.shape
	if len(img_shape)==2:
		return
	else:
		grey_image = original_image.mean(axis=2)
		root.image = grey_image
		plt.imshow(root.image,cmap='gray')
		canvas.show()
		root.update()

#make widgets
Tk.Label (text='Enter a search query:').pack(side=Tk.TOP,padx=10,pady=10)
searchbox = Tk.Entry(root, width=50)
quit_button = Tk.Button(master=root, text='Quit', command=sys.exit)
search_button = Tk.Button(master=root,text='Search', command=search)
url_label = Tk.Label(root,height=3,width=80,justify=Tk.LEFT,\
          textvariable=url_disp,relief=Tk.SUNKEN)
reverse_button=Tk.Button(master=root,text="reverse",command=img_reverse)
rotate_button=Tk.Button(master=root,text="rotate",command=img_rotate)
grey_button=Tk.Button(master=root,text="grey",command=img_grey)

url_disp.set("Url for the image query goes here")
#pack all the widgets
searchbox.pack(side=Tk.TOP,padx=10,pady=10)
quit_button.pack(side=Tk.BOTTOM)
search_button.pack(side=Tk.BOTTOM)
reverse_button.pack(side=Tk.BOTTOM)
rotate_button.pack(side=Tk.BOTTOM)
grey_button.pack(side=Tk.BOTTOM)
url_label.pack(side=Tk.TOP)
Tk.mainloop()