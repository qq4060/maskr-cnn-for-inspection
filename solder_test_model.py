# -*- coding: utf-8 -*-
##### Import COCO config
#sys.path.append(os.path.join(ROOT_DIR, "samples\\coco\\"))  # To find local version
#from samples.coco import coco
#### Directory to save logs and trained model
#MODEL_DIR = os.path.join(ROOT_DIR, "logs\\shapes20190417T1728\\")
 
#### Local path to trained weights file
#COCO_MODEL_PATH = os.path.join(MODEL_DIR ,"mask_rcnn_shapes_0030.h5")

import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import cv2
import time
from mrcnn.config import Config
from datetime import datetime 
# Root directory of the project
ROOT_DIR = os.getcwd()
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
from samples.coco import coco


# Directory to save logs and trained model#
# #shapes20190524T2010 ;shapes20190607T1814

#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190610T1712")#Imagelet
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190610T1851")#coco     TRAIN_ROIS_PER_IMAGE =1000
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1053")#coco     TRAIN_ROIS_PER_IMAGE =500
#MODEL_DIR = os.path.join(ROOT_DIR, "logs/shapes20190607T1814")#coco RAIN_ROIS_PER_IMAGE =100
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1202")#coco     TRAIN_ROIS_PER_IMAGE =50
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1447")#coco     TRAIN_ROIS_PER_IMAGE =30

MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1251")#coco     TRAIN_ROIS_PER_IMAGE =10
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1317")#coco     TRAIN_ROIS_PER_IMAGE =1
#MODEL_DIR = os.path.join(ROOT_DIR, "solder_train_data/shapes20190611T1348")#coco     TRAIN_ROIS_PER_IMAGE =5






# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(MODEL_DIR ,"mask_rcnn_shapes_0030.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)
    print("cuiwei***********************")

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

class ShapesConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "shapes"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 5  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 64
    IMAGE_MAX_DIM = 128

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8 * 6, 16 * 6, 32 * 6, 64 * 6, 128 * 6)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE =100

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 100

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 50

#import train_tongue
#class InferenceConfig(coco.CocoConfig):
class InferenceConfig(ShapesConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

#model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)


# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'good component','no component','component shift','wrong component','tombstone']
# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
#image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
file_names = 'images/12.bmp' # next(os.walk(IMAGE_DIR))[2]
    # image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
image = skimage.io.imread(file_names)

a=datetime.now() 
start = time.time()

# Run detection
results = model.detect([image], verbose=1)
elapsed = (time.time() - start)
print("Time",elapsed)

b=datetime.now() 
# Visualize results
print("Time1",(b-a).seconds)

c=time.time() 

results1 = model.detect([image], verbose=1)

d=time.time() 
print("Time2",(d-c))


r = results[0]
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])
# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
#image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
#cap = cv2.VideoCapture(0)
#
#while(1):
#    # get a frame
#    ret, frame = cap.read()
#    # show a frame
#    start =time.clock()
#    results = model.detect([frame], verbose=1)
#    r = results[0]
#    #cv2.imshow("capture", frame)
#    visualize.display_instances(frame, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'])
#    end = time.clock()
#    print(end-start)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
#cap.release()
#cv2.destroyAllWindows() 

#image= cv2.imread("C:\\Users\\18301\\Desktop\\Mask_RCNN-master\\images\\9.jpg")
## Run detection
#
#results = model.detect([image], verbose=1)
#
#print(end-start)
## Visualize results
#r = results[0]
#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'])

 

## Root directory of the project
#ROOT_DIR = os.getcwd()
#
## Directory to save logs and trained model
#MODEL_DIR = os.path.join(ROOT_DIR, "logs/shapes20180713T1554")
#
## Local path to trained weights file
#COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
## Download COCO trained weights from Releases if needed
#if not os.path.exists(COCO_MODEL_PATH):
#    utils.download_trained_weights(COCO_MODEL_PATH)
#
## Directory of images to run detection on
#IMAGE_DIR = os.path.join(ROOT_DIR, "images")
#
#class ShapesConfig(Config):
#    """Configuration for training on the toy shapes dataset.
#    Derives from the base Config class and overrides values specific
#    to the toy shapes dataset.
#    """
#    # Give the configuration a recognizable name
#    NAME = "shapes"
#
#    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
#    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
#    GPU_COUNT = 1
#    IMAGES_PER_GPU = 1
#
#    # Number of classes (including background)
#    NUM_CLASSES = 1 + 1  # background + 3 shapes
#
#    # Use small images for faster training. Set the limits of the small side
#    # the large side, and that determines the image shape.
#    IMAGE_MIN_DIM = 320
#    IMAGE_MAX_DIM = 384
#
#    # Use smaller anchors because our image and objects are small
#    RPN_ANCHOR_SCALES = (8 * 6, 16 * 6, 32 * 6, 64 * 6, 128 * 6)  # anchor side in pixels
#
#    # Reduce training ROIs per image because the images are small and have
#    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
#    TRAIN_ROIS_PER_IMAGE =100
#
#    # Use a small epoch since the data is simple
#    STEPS_PER_EPOCH = 100
#
#    # use small validation steps since the epoch is small
#    VALIDATION_STEPS = 50
#
##import train_tongue
##class InferenceConfig(coco.CocoConfig):
#class InferenceConfig(ShapesConfig):
#    # Set batch size to 1 since we'll be running inference on
#    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
#    GPU_COUNT = 1
#    IMAGES_PER_GPU = 1
#
#config = InferenceConfig()
#
#model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
#
## Load weights trained on MS-COCO
## model.load_weights(COCO_MODEL_PATH, by_name=True)
#model_path = model.find_last()[0]
#
## Load trained weights (fill in path to trained weights here)
#assert model_path != "", "Provide path to trained weights"
#print("Loading weights from ", model_path)
#model.load_weights(model_path, by_name=True)
#
#class_names = ['BG', 'tank']
#
## Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
#image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
#
## Run detection
#results = model.detect([image], verbose=1)
#
## Visualize results
#r = results[0]
#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'])