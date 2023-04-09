import cv2
import numpy as np
import os
import sys 
import tensorflow as tf 
from tensorflow.keras import layers, models 

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43 
# NUM_CATEGORIES = 3 # for small direc
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
   
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """ 
    """images and labels should be of same size
       each image should have a corresponding label""" 
    # create a list of folders
    folders = os.listdir(data_dir) 

    images = [] 
    labels = [] 

    for folder in folders:  # for all folders 
        folderpath = os.path.join(data_dir, folder)  
        if os.path.isdir(folderpath): 
            files = os.listdir(folderpath)   # create a list of all files of given folder

            for file in files:   # for all files
                filepath = os.path.join(folderpath, file)

                img = cv2.imread(filepath)  # convert to ndarray
                if img is not None:
                    resizedImg = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

                    images.append(resizedImg)
                    labels.append(int(folder)) 

                    # print(resizedImg.shape)
                    # cv2.imshow('image', resizedImg)
                    # cv2.waitKey(0) & 0xFF
                    # cv2.destroyAllWindows() 
    # print(labels)
    return (images, labels) 

    # raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """ 
    """ input shpae should be equal to as input image size
        output units should be equal to no of labels""" 
    # create a sequential neural network 
    CNN = models.Sequential()  

    # first layer = conv + input 
    CNN.add(layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (IMG_WIDTH, IMG_HEIGHT, 3))) 
    
    # max pooling
    CNN.add(layers.MaxPooling2D(2, 2)) 

    # again convolution and max pooling
    CNN.add(layers.Conv2D(64, (3, 3), activation = 'relu')) 
    CNN.add(layers.MaxPooling2D(2, 2)) 
    
    # flatten 3D tensor to 1D vectors 
    CNN.add(layers.Flatten()) 

    #dropout layer 
    CNN.add(layers.Dropout(.2)) 
    CNN.add(layers.Dropout(.2)) 

    # add one more dense layers for classification
    CNN.add(layers.Dense(128, activation = 'relu'))  

    # output layer = dense + output units
    CNN.add(layers.Dense(NUM_CATEGORIES, activation = 'softmax'))  

    CNN.compile(optimizer='adam', 
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # print(CNN.summary()) 
    return CNN
    # raise NotImplementedError


if __name__ == "__main__":
    main()
