Included in this homework is a file called "Image_classification.py"
and a file called "Image_classification.ipynb".  The code in the .ipynb file is identical, but I included it because you mentioned notebooks were more convenient for you.  

To properly work the .py, it assumes the folder called "50_categories" included in the same directory. 
If you run this file it will produce a filed called "trained_classifier.p", which is a file containing the RandomTreeClassifier object produced by running Image_classification.py. 
 I did not included the file trained_classifier.p because it was over 300 mb. 
It took me about an hour to produce it when I run my code on my laptop. 
Image_classification.py includes a function called run_final_classifier().  It takes two arguments as inputs.  The first argument is a string called "path" which is the path to a folder containing test images.  It is assumed that the folder containing the test images contains no subfolders and no files other than the images.  The second argument, "forest" is a RandomTreeClassifier object.  This object is used estimate labels for the images in "path".  

Using cross validation on the training set, I obtained a prediction accuracy of .20 (+/- .02).  With random guessing there are 50 labels that are each equally likely, so the expected random accuracy is .02.  

The function feature_0 computes 2 features: The number of objects and the number of objects of size > 20 when using edge based segmentation.

The function feature_1 computes 3 features: the average local entropy over each color channel

The function feature_2 computes 6 features: the maximum correlation between color channels i and j for all 6 possibilities of i and j

The function feature_3 computes 1 feature: the image size


My features are similar, but I found the computation time to be too large if I didn't compute multiple features in one function call.

I wanted to include additional features counting vertical and horizontal edge objects, but I wasn't able to properly debug them. 