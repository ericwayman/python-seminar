import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from scipy import ndimage
ima = sp.misc.imread('./Data/im1-a.png',flatten=True)
first_dot_pos = np.unravel_index(ima.argmin(),ima.shape)
dot_centers = [first_dot_pos]
offsets = []
shifted_images=[]
masked_images=np.ma.masked_array(np.zeros((288,288,5)))
indx=0
for x in ["a","b","c","d","e"]:
    im = sp.misc.imread('./Data/im1-%s.png' % x,flatten=True) 
    dot_index= np.unravel_index(im.argmin(),im.shape)
    offset= np.subtract(first_dot_pos,dot_index)
    im_shifted = sp.ndimage.interpolation.shift(input=im,shift=offset,mode='wrap')
    im_masked=np.ma.masked_array(im_shifted,mask=(im_shifted==183))
    masked_images[:,:,indx]=im_masked
    sp.misc.imsave('./Data/im1-%s-shift.png' %x,im_shifted)
    sp.misc.imsave('./Data/im1-%s-masked.png' %x,im_masked)
    dot_centers.append(dot_index) 
    offsets.append(offset)
    shifted_images.append(im_shifted)
    indx +=1
#hidden_message=ma.masked_array(np.zeros((288,288)))
hidden_message= np.ma.median(masked_images, axis=2) 
plt.imshow(hidden_message,cmap='gray')
plt.show()
plt.savefig('Heisenberg.png')