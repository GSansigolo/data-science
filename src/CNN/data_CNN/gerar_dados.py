import os
import glob
import os.path as path
import cv2
import numpy as np

dir_positivos = "positivos/"
dir_negativos = "negativos/"
dir = "casos_teste/"

file_paths = glob.glob(path.join(dir_positivos, '*.TIF'))

images_po = [cv2.imread(positivo) for positivo in file_paths]
images_po = np.asarray(images_po)
print (images_po.shape)

file_paths_ne = glob.glob(path.join(dir_negativos, '*.TIF'))

images_neg = [cv2.imread(negativos) for negativos in file_paths]
images_neg = np.asarray(images_neg)
print (images_neg.shape)

file_paths_te = glob.glob(path.join(dir, '*.TIF'))

file_paths_te.sort()

testeX = [cv2.imread(testes) for testes in file_paths_te]
testeX = np.asarray(testeX)
print (testeX.shape)

y_teste = np.array([0,0,0,0,0,1,1,1,1])
y_positivo = np.array([1,1,1,1,1,1,1,1,1])
y_negativo = np.array([0,0,0,0,0,0,0,0,0])

trainX = np.concatenate((images_po, images_neg), axis = 0)
trainY = np.concatenate((y_positivo, y_negativo), axis = 0)

# x = trainX.reshape(18, 48399,3)
#
# # print("X.shape = {}".format(x.shape))
#
# np.savetxt("trainX", trainX)
# np.savetxt("trainX", trainX)

# Fazer o reload
# x = x.reshape(18, 221,219,3)
# print("X.shape = {}".format(x.shape))
