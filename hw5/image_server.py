import SimpleXMLRPCServer
import numpy as np
import sys
import matplotlib.pyplot as plt

def list_to_array(img_list, img_shape):
	"""A helper function that takes a list and a shape and converts back to an image array.
	"""
	img_array = np.asarray(img_list)
	reshaped_img_array = np.reshape(img_array, img_shape)
	return reshaped_img_array

def array_to_list(img_array):
	"""A help function that takes an array as an input and unravels it into a list
	"""	
	img_ravel = np.ravel(img_array)
	return img_ravel.tolist()


class lossless_image_manipulation:
	def mirror_image(self,img_list,img_shape,img_name):
		"""computes the mirror image of an image by reflecting across the y axis
		inputs: img_list: an image stored as a list rather than an array, which cannot be 
							transferred over SimpleXMLRPCServer
				img_shape: a tuple consisting of the dimensions of the image so recover the image array
				img_name: string.  Then name of the image file
		output: A list.  consisting of the y axis reflection of the original.							
		"""
		img_array = list_to_array(img_list,img_shape)

		# compute mirror image for gray scale images
		if len(img_shape)==2:
			list_of_rows = list(img_array)
			list_of_rows_reversed = [row[::-1] for row in list_of_rows]
			reversed_array = np.asarray(list_of_rows_reversed)
			mirror = reversed_array.reshape(img_shape)
		#compute mirror image for RGB channel images
		else:
			mirror = np.zeros(img_shape)
			for i in range(img_shape[2]):
				list_of_rows = list(img_array[:,:,i])
				list_of_rows_reversed = [row[::-1] for row in list_of_rows]
				reversed_array = np.asarray(list_of_rows_reversed)
				mirror[:,:,i] = reversed_array
		plt.imshow(mirror)
   		plt.savefig("%s_mirror_server.png" %img_name)
   		return array_to_list(mirror)

	#just a test function to see how the client server pair works
	def return_gray_scale(self,img_list,img_shape):
		img_array = np.asarray(img_list)
		reshaped_img_array = np.reshape(img_array, img_shape)
		img = reshaped_img_array.mean(axis=2)
		img_ravel = np.ravel(img)
		return img_ravel.tolist()
		# img_shape = tuple(img_shape_list)
		# img_array = np.asarray(img_list)
		# img_array = np.reshape(img_array,img_shape)
		# if len(img_shape)==3:
		# 	print "we've gotten inside the loop and know the image is 3 dimensional"
		# 	img = img_array.mean(axis=2)
		# 	img_ravel = np.ravel(img)
		# 	return list(img_ravel)
		# else:
		# 	return img_list



host, port = "", 5021
server = SimpleXMLRPCServer.SimpleXMLRPCServer((host, port), allow_none=True)
server.register_instance(lossless_image_manipulation())
#server.register_multicall_functions()
#server.register_introspection_functions()
print "about to serve"
server.serve_forever()
