import os
import glob
import os.path as path
import numpy as np
import cv2
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.utils import np_utils
from keras.layers.advanced_activations import LeakyReLU
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# ----- Realiza a leirura das Imagens ------ #
dir_positivos = "data_CNN/positivos/"
dir_negativos = "data_CNN/negativos/"
dir = "data_CNN/casos_teste/"

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


batch_size = 12
epochs = 20
num_classes = 1


# Define o modelo da REDE
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(221, 219,3),padding='same'))

# Add max pooling layer
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(32, activation='relu'))

# Add output layer
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy',  optimizer='adam',  metrics=['accuracy'])

# Print a summary of the model
model.summary()


#----------------

# model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(221, 219,3),padding='same'))
# model.add(MaxPooling2D((2, 2),padding='same'))
# model.add(Flatten())
# model.add(Dense(32, activation='relu'))
# # model.add(Dense(num_classes, activation='sigmoid'))
# model.add(Dense(1, activation='sigmoid'))
#
# model.compile(loss='categorical_crossentropy', optimizer='sgd',metrics=['accuracy'])
#
# model.summary()

#----------------

# Inicia o treinamento
train_result = model.fit(trainX, trainY, batch_size=batch_size,epochs=epochs,verbose=1, validation_split=0.1)

test_eval = model.evaluate(testeX, y_teste, verbose=1)


print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])

# model.save_weights('classificacao.h5')

# model.load_weights('classificacao.h5', by_name=True)


test_predictions = model.predict(testeX)
# test_predictions = np.round(test_predictions)

# test_predictions = np.argmax(np.round(test_predictions),axis=1)
correct = np.where(test_predictions==y_teste)

print("Found {} correct labes".format(correct))
# print ("correct {}".format(enumerate(correct)))
# print ("correct {}".format(correct))
#
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(testeX[i], interpolation='none')
    plt.title("Predicted {}, Class {}".format(test_predictions[i], y_teste[i]))

plt.show()
