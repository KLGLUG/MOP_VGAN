import numpy as np
import os
from glob import glob
import shutil
from datetime import datetime
from scipy.ndimage import imread

##
# Data
##

def get_date_str():
    """
    @return: A string representing the current date/time that can be used as a directory name.
    """
    return str(datetime.now()).replace(' ', '_').replace(':', '.')[:-10]

def get_dir(directory):
    """
    Creates the given directory if it does not exist.

    @param directory: The path to the directory.
    @return: The path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clear_dir(directory):
    """
    Removes all files in the given directory.

    @param directory: The path to the directory.
    """
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        try:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(e)

# def get_test_frame_dims():
#     img_path = glob(os.path.join(TEST_DIR, '*/*'))[0]
#     img = imread(img_path, mode='RGB')
#     shape = np.shape(img)
#
#     # noinspection PyUnresolvedReferences
#     return shape[0], shape[1]
#
# def set_test_dir(directory):
#     """
#     Edits all constants dependent on TEST_DIR.
#
#     @param directory: The new test directory.
#     """
#     global TEST_DIR, TEST_HEIGHT, TEST_WIDTH
#
#     TEST_DIR = directory
#     TEST_HEIGHT, TEST_WIDTH = get_test_frame_dims()

# root directory for all data
DATA_DIR = get_dir('../Data/')
# path to train data file
TRAIN_PATH = os.path.join(DATA_DIR, 'train.csv')
# path to test data file
TEST_PATH = os.path.join(DATA_DIR, 'test.csv')
# directory of frames
FRAME_DIR = os.path.join(DATA_DIR, 'Frames/')

# num data points in total
NUM_DATA = 99982
# num test data points
NUM_TEST = 1000
# num train data points
NUM_TRAIN = NUM_DATA - NUM_TEST

# the height and width of the full frames to test on. Set in avg_runner.py main.
FRAME_HEIGHT = 210
FRAME_WIDTH = 160

##
# Output
##

def set_save_name(name):
    """
    Edits all constants dependent on SAVE_NAME.

    @param name: The new save name.
    """
    global SAVE_NAME, MODEL_SAVE_DIR, SUMMARY_SAVE_DIR, IMG_SAVE_DIR

    SAVE_NAME = name
    MODEL_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Models', SAVE_NAME))
    SUMMARY_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Summaries', SAVE_NAME))
    IMG_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Images', SAVE_NAME))

def clear_save_name():
    """
    Clears all saved content for SAVE_NAME.
    """
    clear_dir(MODEL_SAVE_DIR)
    clear_dir(SUMMARY_SAVE_DIR)
    clear_dir(IMG_SAVE_DIR)


# root directory for all saved content
SAVE_DIR = get_dir('../Save/')

# inner directory to differentiate between runs
SAVE_NAME = 'Default/'
# directory for saved models
MODEL_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Models', SAVE_NAME))
# directory for saved TensorBoard summaries
SUMMARY_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Summaries', SAVE_NAME))
# directory for saved images
IMG_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Images', SAVE_NAME))

STATS_FREQ      = 10     # how often to print loss/train error stats, in # steps
SUMMARY_FREQ    = 100    # how often to save the summaries, in # steps
IMG_SAVE_FREQ   = 100   # how often to save generated images, in # steps
TEST_FREQ       = 5000   # how often to test the model on test data, in # steps
MODEL_SAVE_FREQ = 1000  # how often to save the model, in # steps

##
# General training
##

# whether to use adversarial training vs. basic training of the generator
# ADVERSARIAL = True
ADVERSARIAL = False
# the training minibatch size
BATCH_SIZE = 8

##
# Loss parameters
##

# for lp loss. e.g, 1 or 2 for l1 and l2 loss, respectively)
L_NUM = 2
# the power to which each gradient term is raised in GDL loss
ALPHA_NUM = 1
# the percentage of the adversarial loss to use in the combined loss
LAM_ADV = 0.05
# the percentage of the lp loss to use in the combined loss
LAM_LP = 1
# the percentage of the GDL loss to use in the combined loss
LAM_GDL = 1

##
# Generator model
##

# learning rate for the generator model
LRATE_G = 0.000005  # Value in paper is 0.04
# padding for convolutions in the generator model
PADDING_G = 'SAME'
# layer sizes for each fully-connected layer of each scale network in the discriminator model
# SCALE_FC_LAYER_SIZES_G = [[6, 1024, 160 * 210 * 256],
#                           [6, 1024, 160 * 210 * 256],
#                           [6, 2048, 160 * 210 * 512],
#                           [6, 2048, 160 * 210 * 512]]

SCALE_FC_LAYER_SIZES_G = [[6, 2048, 160 * 210]]

# feature maps for each convolution of each scale network in the generator model
# e.g SCALE_CONV_FMS_G[1][2] is the input of the 3rd convolution in the 2nd scale network.
# SCALE_CONV_FMS_G = [[256, 128, 3],
#                     [256, 128, 3],
#                     [512, 256, 128, 3],
#                     [512, 256, 128, 3]]

SCALE_CONV_FMS_G = [[1, 128, 256, 512, 256, 128, 3]]

# kernel sizes for each convolution of each scale network in the generator model
# SCALE_KERNEL_SIZES_G = [[3, 3],
#                         [3, 5],
#                         [3, 3, 5],
#                         [5, 5, 7]]

SCALE_KERNEL_SIZES_G = [[5, 5, 7, 7, 5, 5]]


##
# Discriminator model
##

# learning rate for the discriminator model
LRATE_D = 0.02
# padding for convolutions in the discriminator model
PADDING_D = 'VALID'
# feature maps for each convolution of each scale network in the discriminator model
SCALE_CONV_FMS_D = [[3, 64],
                    [3, 64, 128, 128],
                    [3, 128, 256, 256],
                    [3, 128, 256, 512, 128]]
# kernel sizes for each convolution of each scale network in the discriminator model
SCALE_KERNEL_SIZES_D = [[3],
                        [3, 3, 3],
                        [5, 5, 5],
                        [7, 7, 5, 5]]
# layer sizes for each fully-connected layer of each scale network in the discriminator model
# layer connecting conv to fully-connected is dynamically generated when creating the model
SCALE_FC_LAYER_SIZES_D = [[512, 256, 1],
                          [1024, 512, 1],
                          [1024, 512, 1],
                          [1024, 512, 1]]
