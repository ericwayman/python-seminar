import matplotlib.pyplot as plt
import matplotlib
import scipy as sp
import numpy as np
from scipy import ndimage, signal
from scipy.signal import fftconvolve as fftc

#gets the image files
def get_im(x):
    #get image x 
    im = sp.misc.imread('./Data/im2-%s.png' %x,flatten=True)
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
plt.show()
plt.savefig('image_denoising.png')