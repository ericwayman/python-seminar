Included in the homework for problems 1 are the files 
image_client.py
image_server.py

image_server.py creates a SimpleXMLRPCServer with three methods to perform 
lossless image manipulation on an input image.
They are able handle both 2d (grayscale) and 3d (RGB channel) image arrays.
mirror_image(): returns the reflection about the y axis of the image
invert_color_channels(): inverts the value of each color channel
permute_color_channels():cyclically permutes the values of each color channel 


image_client.py contains 3 functions call_mirror_image(), call_invert_color_channels(), and call_permute_color_channels() 
which connect the client to the server and call the functions mirror_image(),
invert_color_channels() and permute_color_channels() resp.

These functions take a path to the image and a name * for the files.
The images will be saved on the client side as *_mirror_client.png,
*_invert_client.png and *_permute_client.png on the client side and *_mirror_server.png, *_invert_server.png and *_permute_server.png on the server side.  
I include an image "test_img.jpg" with *="test" as examples.  