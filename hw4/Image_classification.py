#import relevant modules
import skimage.io as io
import numpy as np
import re, sklearn
import pickle
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
def feature_0(img):
    """Computes the number of objects using edge-based segmentation.
    """
    from scipy import ndimage
    from skimage.filter import canny
    # if image is color, flatten the image to give a greyscale image
    if img.ndim == 3:
        img = img.mean(axis=2)
    edges = canny(img/255.)
    fill_img = ndimage.binary_fill_holes(edges)
    label_objects, num_obj = ndimage.measurements.label(fill_img)
    return num_obj

def feature_1(img):
    """Computes the number of large objects using edge-based segmentation.
    Here a large object is one of size > 20
    """
    from scipy import ndimage
    from skimage.filter import canny
    # if image is color, flatten the image to give a greyscale image
    if img.ndim ==3:
        img = img.mean(axis=2)
    edges = canny(img/255.)
    fill_img = ndimage.binary_fill_holes(edges)
    label_objects, num_obj = ndimage.measurements.label(fill_img)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20
    mask_sizes[0] = 0
    img_cleaned = mask_sizes[label_objects]
    big_label_objects, big_num_obj = ndimage.measurements.label(img_cleaned)
    return big_num_obj
def feature_2(img): 
    """Computes the average local entropy over each pixel of the image.  
    The local entropy is computed over a disc of radius 5, and is an average of the local entropy over 
    the RGB channels or greyscale image if 2D
    input: a color or greyscale image img. 
    returns: a float representing the average local entropy of the image.
    """
    import numpy as np
    from skimage.filter.rank import entropy
    from skimage.morphology import disk
    if img.ndim==3:
        ent_array = np.zeros(img.shape[0:2])
        for i in [0,1,2]:
            ent_array += entropy(img[:,:,i],disk(5))
        return np.mean(ent_array)/3.0
    else:
        ent_array = entropy(img,disk(5))
        return np.mean(ent_array)

def feature_3(img,i=0,j=1):
    """Computes the maximum cross correlation between color channels i and j in the image
    inputs: a 3 color channel image: img, the indices of the channels for which the cross cor is computed: i,j
    returns: the maximum correlation of the normalized images corresponding to channels i and j
    """
    import numpy as np
    from scipy.signal import fftconvolve as fftc
    #If only one color channel just return 0
    if img.ndim==2:
        return 0
    else:
        img_1 = img[:,:,i]
        img_2 = img[:,:,j]
        #normalize the two color channels
        im1_norm = (img_1-img_1.mean())/img_1.std()
        im2_norm = (img_2-img_2.mean())/img_2.std()
        corr = fftc(im1_norm,im2_norm, mode = 'same') #cross cor of the base image
        return np.max(corr)



def compute_features(img, num_feat=4):
    """
    inputs: num_feat and integer representing the number of features to compute.
    image: a 3 dim RGB image array on which to compute a list of features.
    Returns: a list of length num_feat containing the computed features for the image 
    Assumes the features are given by functions labeled "feature_i" for i=0,..,num_feat-1
    and that these feature functions return a float valued feature.
    """
    feature_list =[0]*num_feat
    for i in range(num_feat):
        func_name = 'feature_%s' %str(i)
        feature = globals()[func_name](img)
        feature_list[i]=feature
    #or to avoid the loop it might be faster if we replace it with lines like
    #feature_list[0]=feature_0(img)
    #feature_list[1]=feature_1(img)
    #feature_list[2]=feature_2(img)
    #feature_list[3]=feature_3(img)    
    return feature_list
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

def extract_training_features(image_path_list):
    """
    inputs: image_path_list: a directory containing images files to be extracted
    Returns: feature_list a list of length equal to the number of images in image_path_list
        Each element of feature list is a list containing the path to the image and the features 
        for the corresponding image
        Keeps the path and features grouped together so we can shuffle the list and keep the
        image path and correpsonding features together
    """
    path_feat_list = []
    for image_path in image_path_list:
        image_array = imread(image_path)
        feature_list = compute_features(image_array)
        feature_list.insert(0,image_path)
        path_feat_list.append(feature_list)
    return path_feat_list

def extract_test_features(image_path_list):
    """
    This function is similar to extract_training_features, except we only extract a list of features
    we don't include the image paths because we don't need the labels
    inputs: image_path_list: a directory containing images files to be extracted
    Returns: feature_list a list of length equal to the number of images in image_path_list
        Each element of feature list is a list containing the path to the image and the features 
        for the corresponding image
        Keeps the path and features grouped together so we can shuffle the list and keep the
        image path and correpsonding features together
    """
    path_feat_list = []
    for image_path in image_path_list:
        image_array = imread(image_path)
        feature_list = compute_features(image_array)
        path_feat_list.append(feature_list)
    return path_feat_list



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
result = p.map_async(extract_training_features, split_image_paths)
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
#print "the first labels of the first five samples are: "+ str(targ_lab_keys[0:5])
#print "the first label values of the first five samples are: "+str(targ_lab_vals[0:5])
#print "The features of the first five samples are: "+ str(X[0:5,:])

#Make the Random tree classifier 
clf = RandomForestClassifier(n_estimators=50,n_jobs=-1,compute_importances=True)
clf = clf.fit(X,targ_array)
#print "The 50 Label classes are:"+str(clf.classes_)
scores = sklearn.cross_validation.cross_val_score(clf,X,targ_array)
print("Accuracy: %.2f (+/-%.2f)" %(scores.mean(),scores.std()*2))
print scores
pickle.dump(clf, open('trained_classifier.p','w'))

def run_final_classifier(path,forest):
    """Using the Random forest classifier model trained on the images in the folder
    '50_categories', this function returns and prints the predictions for the labels
    from the images located in 'path'.
    inputs: path: the path where the test images are located.  
                Assumes all test images are located in a single directory in path
                that is, none of the images should be located in subdirectories within path
            forest: the RandomForestClassifier object trained on the image set in 
                    '50_categories'
    Returns: The predicted labels for the images in path.                                    
    """
    label_dict =   {
    0: 'airplanes', 1: 'bat', 2: 'bear', 3: 'blimp', 4: 'camel', 5: 'comet', 6: 'conch', 7: 'cormorant', 8: 
    'crab', 9: 'dog', 10: 'dolphin', 11: 'duck', 12: 'elephant', 13: 'elk', 14: 'frog', 15: 'galaxy', 16: 
    'giraffe', 17: 'goat', 18: 'goldfish', 19: 'goose', 20: 'gorilla', 21: 'helicopter', 22: 'horse', 23: 
    'hot-air-balloon', 24: 'hummingbird', 25: 'iguana', 26: 'kangaroo', 27: 'killer-whale', 28: 'leopards', 
    29: 'llama', 30: 'mars', 31: 'mussels', 32: 'octopus', 33: 'ostrich', 34: 'owl', 35: 'penguin', 36: 
    'porcupine', 37: 'raccoon', 38: 'saturn', 39: 'skunk', 40: 'snail', 41: 'snake', 42: 'speed-boat', 
    43: 'starfish', 44: 'swan', 45: 'teddy-bear', 46: 'toad', 47: 'triceratops', 48: 'unicorn', 49: 'zebra'
    }


    image_paths = []
    file_name_list = []
    image_names = listdir(path)
    for name in image_names:
        image_paths.append(path + "/" + name)
        file_name_list.append(name)
    print ("collected pathes for %s test images" %str(len(image_paths)))
    

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
    result = p.map_async(extract_test_features, split_image_paths)
    poolresult = result.get()
    end_time = time()

    # All done, print timing results.
    print ("Finished extracting features. Total time: " + 
        str(round(end_time-start_time, 3)) + " s, or " + 
        str( round( (end_time-start_time)/len(image_paths), 5 ) ) + " s/image.")


    # To tidy-up a bit, we loop through the poolresult to create a final list of
    # the feature extraction results for all images.
    combined_result = []
    for single_proc_result in poolresult:
        for single_image_result in single_proc_result:
            combined_result.append(single_image_result)
    test_feat_array = np.array(combined_result)
    prediction = forest.predict(test_feat_array)
    print("the first 5 predicted numeric labels are:")
    print prediction[0:5]
    print("filename       predicted_class")
    print("________________________________")
    for i in range(len(file_name_list)):
        print("%s          %s" %(file_name_list[i],label_dict[prediction[i]]))
#path = './50_categories/airplanes'
#run_final_classifier(path,clf)
