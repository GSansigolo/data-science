
# https://medium.com/@kylepob61392/airplane-image-classification-using-a-keras-cnn-22be506fdb53

import glob
import numpy as np
import matplotlib.pyplot as plt
import os.path as path
from scipy import misc


def visualize_data(positive_images, negative_images):
    # INPUTS
    # positive_images - Images where the label = 1 (True)
    # negative_images - Images where the label = 0 (False)

    figure = plt.figure()
    count = 0
    for i in range(positive_images.shape[0]):
        count += 1
        figure.add_subplot(2, positive_images.shape[0], count)
        plt.imshow(positive_images[i, :, :])
        plt.axis('off')
        plt.title("1")

        figure.add_subplot(1, negative_images.shape[0], count)
        plt.imshow(negative_images[i, :, :])
        plt.axis('off')
        plt.title("0")
    plt.show()

image_path = "/home/fabiana/Documentos/Mestrado/mydevel/2_periodo/CAP-240-394/src/data/20x20"
file_paths = glob.glob(path.join(image_path, '*.png'))

# print file_paths

# Load the images into a single variable and convert to a numpy array
images = [misc.imread(path,flatten=True) for path in file_paths]
images = np.asarray(images)

# Get image size
image_size = np.asarray([images.shape[0], images.shape[1], images.shape[2]])
print(image_size)

# Scale
images = images / 255

n_images = images.shape[0]
labels = np.zeros(n_images)

for i in xrange(10):
    labels[i] = 1

# print labels

# Split into test and training sets
TRAIN_TEST_SPLIT = 0.8

# Split at the given index
split_index = int(TRAIN_TEST_SPLIT * n_images)
shuffled_indices = np.random.permutation(n_images)
train_indices = shuffled_indices[:split_index]
test_indices = shuffled_indices[split_index:]

print ("train_indices {}".format(train_indices))
print ("test_indices {}".format(test_indices))

# Split the images and the labels
# x_train = images[train_indices, :, :]
# y_train = labels[train_indices]
# x_test = images[test_indices, :, :]
# y_test = labels[test_indices]
#
#
# print ("x_train.shape {}".format(x_train.shape))
# print ("y_train.shape {}".format(y_train.shape))
#
# print ("x_test.shape {}".format(x_test.shape))
# print ("y_test.shape {}".format(y_test.shape))
#
# print ("y_train: {}".format(y_train))
# print ("y_test: {}".format(y_test))
#
# # Number of positive and negative examples to show
# N_TO_VISUALIZE = 3
# #
# # Select the first N positive examples
# positive_example_indices = (y_train == 1)
# print ("positive_example_indices: {}".format(np.sum(positive_example_indices)))
# print positive_example_indices
#
#
# positive_examples = x_train[positive_example_indices, :, :]
#
# print ("positive_examples: {}".format(positive_examples.shape))
# print positive_examples[:1, :, :]
# positive_examples_sample = positive_examples[:, :, :]
#
# print ("positive_examples2: {}".format(positive_examples_sample.shape))
#
# for i in range(np.sum(positive_example_indices)):
#     image = positive_examples_sample = positive_examples[i, :, :]
#     print ("positive_examples: {} shape {}".format(i, image.shape))
#     plt.imshow(image)
#     plt.show()
#
#
# positive_examples = positive_examples[0:N_TO_VISUALIZE, :, :]

#
# Select the first N negative examples
# negative_example_indices = (y_train == 0)
# print ("negative_example_indices: {}".format(np.sum(negative_example_indices)))
# negative_examples = x_train[negative_example_indices, :, :]
# negative_examples = negative_examples[0:N_TO_VISUALIZE, :, :]
# #
# # Call the visualization function
# visualize_data(positive_examples, negative_examples)
