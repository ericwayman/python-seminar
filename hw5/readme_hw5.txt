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

Include in the homework for problem 2 is the file 
note_identifier.py
This function takes the path a .aif sound file and the sound file name as an input.
It prints the value of the peak frequency, the nearest musical note frequency and the 
corresponding musical note.
Also included are plots of the amplitude with respect to time and  the frequency
power spectrum for each sound file.
I was unable to find a way to effectively extract the top 3 notes.  I tried using scipy.signal.find_peaks_cwt() to smooth the fft and extract the peaks, but it ran too slowly.  Also included are the plots for a few of the sound files.
The main notes computed from the test sound files are:

The C0 values seem to be caused by negative frequencies.  Need to restrict the argmax() to positive frequencies only!  Also there seemed to be a lot of noise from my plots of the amplitudes.  I wasn't sure how to fix this.
1.aif:G4
2.aif:C0
3.aif:C0
4.aif:C0
5.aif:C0
6.aif:G6
7.aif:A6
8.aif:F5
9.aif: G4
10.aif: C0
11.aif: E6
12.aif: C0