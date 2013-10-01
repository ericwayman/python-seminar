#import relevant modules
import skimage.io as io
import numpy as np
import re, sklearn
from sklearn.ensemble import RandomForestClassifier
from os import listdir
from multiprocessing import Pool, cpu_count
from pylab import imread
from time import time


#Methods to compute image features




#Build up Training Data

#path to the folders of image categories
#MYDIRECTORY = '/Users/waymaniac/Desktop/Py_for_data_sci/homework/hw4/50_categories'
MYDIRECTORY = './50_categories'

# FUNCTION DEFINITIONS


####FEATURE FUNCTIONS
#these functions compute and return a real numbered value feature of an image
#all these functions take a 3d image array as an input and return a 
#float representing an image feature as an output
def feature_1(img):
    """Computes the number of objects using edge-based segmentation.
    """
    from scipy import ndimage
    from skimage.filter import canny
    #flatten the image to give a greyscale image
    flat_img = img.mean(axis=2)
    edges = canny(flat_img/255.)
    fill_img = ndimage.binary_fill_holes(edges)
    label_objects, num_obj = ndimage.measurements.label(fill_img)
    return num_obj

def feature_2(img):
    """Computes the number of large objects using edge-based segmentation.
    Here a large object is one of size > 20
    """
    from scipy import ndimage
    from skimage.filter import canny
    #flatten the image to give a greyscale image
    flat_img = img.mean(axis=2)
    edges = canny(flat_img/255.)
    fill_img = ndimage.binary_fill_holes(edges)
    label_objects, num_obj = ndimage.measurements.label(fill_img)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20
    mask_sizes[0] = 0
    img_cleaned = mask_sizes[label_objects]
    big_label_objects, big_num_obj = ndimage.measurements.label(img_cleaned)
    return big_num_obj




# Quick function to divide up a large list into multiple small lists, 
# attempting to keep them all the same size. 
def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
            newseq.append(seq[int(round(i*splitsize)):
                int(round((i+1)*splitsize))])
        return newseq
# Our simple feature extraction function. It takes in a list of image paths, 
# does some measurement on each image, then returns a list of the image paths
# paired with the results of the feature measurement.

def compute_features(image):
    """
    """

def extract_features(image_path_list):
    """inputs: image_path_list: a directory containing images files to be extracted
        outputs: feature_list a list of length equal to the number of images in image_path_list
        Each element of feature list is a list containing the path to the image and the features 
        for the corresponding image
    """
    feature_list = []
    for image_path in image_path_list:
        image_array = imread(image_path)
        feature = image_array.size # This feature is simple. You can modify this
        feature2 = np.mean(image_array)
        # code to produce more complicated features and to produce multiple
        # features in one function call.
        #feature = avg_entropy(image_array)
        #feature3 = color_cross_cor(image_array,i=0,j=1)
        feature_list.append([image_path, feature, feature2])
    return feature_list




### Main program starts here ###################################################
###This program trains a random tree classifier model
### on the images in the folder 50_categories and estimates the accuracy 
###using cross validation




# We first collect all the local paths to all the images in one list
image_paths = []
keys = []
categories = listdir(MYDIRECTORY)
for category in categories:
    #make sure we don't grab the .DS_Store file which isn't a directory
    if category != '.DS_Store':
    	keys.append(category)
        image_names = listdir(MYDIRECTORY  + "/" + category)
    	for name in image_names:
        	image_paths.append(MYDIRECTORY + "/" + category + "/" + name)
print ("There should be 4244 images, actual number is " + 
    str(len(image_paths)) + ".")
values = range(len(keys))
label_dict = dict(zip(keys,values))
print ("the dictionary for the classification labels: " + str(label_dict))

# Then, we run the feature extraction function using multiprocessing.Pool so 
# so that we can parallelize the process and run it much faster.
numprocessors = cpu_count() # To see results of parallelizing, set numprocessors
                            # to less than cpu_count().
# numprocessors = 1

# We have to cut up the image_paths list into the number of processes we want to
# run. 
split_image_paths = split_seq(image_paths, numprocessors)

# Ok, this block is where the parallel code runs. We time it so we can get a 
# feel for the speed up.
start_time = time()
p = Pool(numprocessors)
result = p.map_async(extract_features, split_image_paths)
poolresult = result.get()
end_time = time()

# All done, print timing results.
print ("Finished extracting features. Total time: " + 
    str(round(end_time-start_time, 3)) + " s, or " + 
    str( round( (end_time-start_time)/len(image_paths), 5 ) ) + " s/image.")
# This took about 10-11 seconds on my 2.2 GHz, Core i7 MacBook Pro. It may also
# be affected by hard disk read speeds.

# To tidy-up a bit, we loop through the poolresult to create a final list of
# the feature extraction results for all images.
combined_result = []
for single_proc_result in poolresult:
    for single_image_result in single_proc_result:
        combined_result.append(single_image_result)


#Split the results into an array of the sample labels: label_list
# and an array of the sample features: X
np.random.shuffle(combined_result)
result_array = np.array(combined_result)
print "The first 5 samples from the result are are:  "+ str(result_array[0:5,])
Y = result_array[:,0]
X = result_array[:,1:]
regex = re.compile('50_categories/(.*?)/')
#find the list of labels in the 4244 training images
targ_lab_keys = [regex.search(Y[i]).group(1) for i in range(len(Y))]
#return the integer keys associated with each label in the training images
targ_lab_vals = [label_dict.get(val) for val in targ_lab_keys] 
#convert the list of label keys to an array to be used for the scikit functions
targ_array = np.asarray(targ_lab_vals)
print "the first labels of the first five samples are: "+ str(targ_lab_keys[0:5])
print "the first label values of the first five samples are: "+str(targ_lab_vals[0:5])
print "The features of the first five samples are: "+ str(X[0:5,:])

#Make the Random tree classifier 
clf = RandomForestClassifier(n_estimators=50,n_jobs=-1,compute_importances=True)
#clf = clf.fit(X,targ_lab_vals)
#print "The 50 Label classes are:"+str(clf.classes_)
scores = sklearn.cross_validation.cross_val_score(clf,X,targ_array)
print("Accuracy: %.2f (+/-%.2f)" %(scores.mean(),scores.std()*2))
print scores


def run_final_classifier(path,forest):
    """Using the Random forest classifier model trained on the images in the folder
    '50_categories', this function returns and prints the predictions for the labels
    from the images located in 'path'.
    inputs: path: the path where the test images are located.
            forest: the RandomForestClassifier object trained on the image set in 
                    '50_categories'
    outputs: The predicted labels for the images in path.                                    
    """



