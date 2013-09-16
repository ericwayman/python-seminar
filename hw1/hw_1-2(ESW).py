# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Due Wednesday Sept 11, 2013 @ 5pm ##
# 
# Send us an email `ucbpythonclass+seminar@gmail.com` (with a tarball of notebook/code/files)
# 
# ## Super-resolution imaging ##
# 
# Obtaining several snapshots of the same scene, from microscopes to telescopes, is useful for the postprocessing increase of signal to noise: by summing up imaging data we can effectively beat down the noise. Interestingly, if we image the same scene from different vistas we can also improve the clarity of the combined image. Being able to discern features in a scene from this combination effort is sometimes called super-resolution imaging.
# 
# Here, we'll combine about 4 seconds of a shaky video to reveal the statement on a license plate that is not discernable in any one frame.
# 
# <img src="files/hw_0_data/im2-1.png">

# <markdowncell>

# A tarball of the data is at: https://www.dropbox.com/s/0clmmvwkoy000d4/homework1_data.tgz
# 
# 1) Resize each frame to be 3 times larger in each axis (ie. 9 times larger images). Using `scipy.signal.correlate2d` find the offsets of each frame with respect to the first frame. Report those offsets to 2 decimal places.

# <markdowncell>

# 2) shift each image to register the frames to the original (expanded in size) frame. You should, in general, be shifting by subpixel offsets.

# <markdowncell>

# 3) Combine all the registered images to form a super-resolution image. What does the license plate read?

# <codecell>

import pylab 
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from scipy import ndimage, signal
from scipy.signal import fftconvolve as fftc

#gets the image files
def get_im(x):
    #get image x 
    im = sp.misc.imread('./Desktop/Py_for_data_sci/Data/im2-%s.png' %x,flatten=True)
    return im

#returns the zoomed, cropped and normalized image on which we will find the cross correlations
def normalize_im(im):
    im_zoom = sp.ndimage.interpolation.zoom(input=im,zoom=3)
    im_crop = im_zoom[175:700,:]
    im_normalized = (im_crop - im_crop.mean())/im_crop.std()
    return im_normalized

im0=get_im(0)
im0_norm = normalize_im(im0)
corr00 = fftc(im0_norm,im0_norm, mode = 'same')
baseline = np.unravel_index(corr00.argmax(),corr00.shape) #find the max of the cross cor of base image 
images_shift = np.zeros((im0.shape[0],im0.shape[1],100))
offsets=[]
for x in range(0,100):
    im = get_im(x)
    im_norm = normalize_im(im)
    corr = fftc(im0_norm,im_norm,mode = 'same')
    offset = np.unravel_index(corr.argmax(),corr.shape)
    offset = np.subtract(baseline,offset)
    offsets.append(offset)
    images_shift[:,:,x]=sp.ndimage.interpolation.shift(input=im,shift=offset/3)
  
crisp_im = np.ma.median(images_shift, axis=2) 


fig, (ax1,ax2) = plt.subplots(1,2)
ax1.imshow(crisp_im,cmap='gray')
ax2.imshow(im0,cmap='gray')

# <codecell>


