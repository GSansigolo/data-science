
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.utils import np_utils
from sklearn.metrics import accuracy_score, f1_score


X_train = np.loadtxt('../../data/res/trainX')
y_train = np.loadtxt('../../data/res/trainY')

X_test = np.loadtxt('../../data/res/testX')
y_test = np.loadtxt('../../data/res/testY')

print ("X_train.shape {}".format(X_train.shape))
print ("X_train.shape[0] {}".format(X_train.shape[0]))
print ("y_train.shape {}".format(y_train.shape))
print ("X_test.shape {}".format(X_test.shape))
print ("y_test.shape {}".format(y_test.shape))

sizeInput = X_train.shape[1]
print ("Camada de Entrada {}".format(sizeInput))


# Network
model = Sequential([
        Dense(512, input_shape=(sizeInput,)),
        Activation('sigmoid'),
        Dense(10),
        Activation('softmax')
    ])

# Compile
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# Learning
model.fit(X_train, y_train, batch_size=200, verbose=1, epochs=20, validation_split=0.1)

# Forecast
score = model.evaluate(X_test, y_test, verbose=1)
print('test accuracy : ', score[1])

# Make a prediction on the test set
test_predictions = model.predict(X_test)
test_predictions = np.round(test_predictions)


# for result in test_predictions:
#     print ("Result {}".format(result.argmax()))


figure = plt.figure()
maximum_square = 4
count = 0
for i in range(12):
    count =  count + 1
    figure.add_subplot(maximum_square, maximum_square, count)
    plt.imshow(X_test[i:i + 1,:].reshape(20,20))
    plt.axis('off')
    predict = test_predictions[i + 1].argmax()
    real = y_test[i + 1].argmax()
    plt.title("Predicted: " + str(int(predict)) + ", Real: " + str(int(real)), fontsize=10)

plt.show()
