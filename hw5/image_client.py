import xmlrpclib
import numpy as np
from pylab import imread, imshow
import matplotlib.pyplot as plt

#s = xmlrpclib.ServerProxy("http://localhost:5021/")

#img_path="./test_image.jpg"

#helper function
def read_to_list(img_path):
	"""Reads an image and converts it to a string to be transferred to the server
	input: img_path a string. The path to the image
	outputs: img_ravel a string representation of the image
			nd_img_shape a tuple representing the shape of the original image
	"""
	nd_img_array = imread(img_path)
	nd_img_shape = nd_img_array.shape
	nd_img_ravel = np.ravel(nd_img_array)
	img_ravel = nd_img_ravel.tolist()
	return img_ravel, nd_img_shape

def call_mirror_image(img_path, img_name):
	"""
	calls mirror_image from the server using the img located at img_path as an input.
	Saves the image returned by mirror_image on the client side
	inputs: img_path a string. The path to the image
			img_name a string. The name of the image
	"""

	img_ravel, nd_img_shape = read_to_list(img_path)

	#connect to server
	s = xmlrpclib.ServerProxy("http://localhost:5021/")
	#call server function
	result = s.mirror_image(img_ravel, nd_img_shape, img_name)
	#convert the list back to an image array
	nd_result = np.asarray(result)
	reshaped_nd_result = np.reshape(nd_result, nd_img_shape)

	#plot and save the image
	plt.imshow(reshaped_nd_result, cmap='gray')
	plt.savefig("%s_mirror_client.png" %img_name)

def call_invert_color_channels(img_path, img_name):
	"""
	calls invert_color_channels from the server using the img located at img_path as an input.
	Saves the image returned by invert_color_channels on the client side
	inputs: img_path a string. The path to the image
			img_name a string. The name of the image
	"""

	img_ravel, nd_img_shape = read_to_list(img_path)

	#connect to server
	s = xmlrpclib.ServerProxy("http://localhost:5021/")
	#call server function
	result = s.invert_color_channels(img_ravel, nd_img_shape, img_name)
	#convert the list back to an image array
	nd_result = np.asarray(result)
	reshaped_nd_result = np.reshape(nd_result, nd_img_shape)

	#plot and save the image
	plt.imshow(reshaped_nd_result, cmap='gray')
	plt.savefig("%s_invert_client.png" %img_name)

def call_permute_color_channels(img_path, img_name):
	"""
	calls permute_color_channels from the server using the img located at img_path as an input.
	Saves the image returned by invert_color_channels on the client side
	inputs: img_path a string. The path to the image
			img_name a string. The name of the image
	"""

	img_ravel, nd_img_shape = read_to_list(img_path)

	#connect to server
	s = xmlrpclib.ServerProxy("http://localhost:5021/")
	#call server function
	result = s.permute_color_channels(img_ravel, nd_img_shape, img_name)
	#convert the list back to an image array
	nd_result = np.asarray(result)
	reshaped_nd_result = np.reshape(nd_result, nd_img_shape)

	#plot and save the image
	plt.imshow(reshaped_nd_result, cmap='gray')
	plt.savefig("%s_permute_client.png" %img_name)

if __name__== "__main__":
	"""Function to be run in the terminal.  Should include two arguments at command line,
	both are strings so don't forget quotes around them.  
	first argument is the path to the image file.  Second is the name you want for the output files
	Running this function will run all 3 image manipulation functions.
	"""
	import argparse
	parser=argparse.ArgumentParser(description="Send an image to server for lossless manipulation")
	parser.add_argument("path",
						type =str,
						nargs=1,
						help="a string that is path for an image file to be sent to server. Don't forget quotes",
						metavar="PATH")
	parser.add_argument("name",
						type =str,
						nargs=1,
						help="a string that is a name for the image. Don't forget quotes",
						metavar="NAME")
	args = parser.parse_args()
	call_mirror_image("".join(args.path),"".join(args.name))
	call_invert_color_channels("".join(args.path),"".join(args.name))
	call_permute_color_channels("".join(args.path),"".join(args.name))


