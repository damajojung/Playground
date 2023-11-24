#import tensorflow as tf
import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense

class DogsVSCats():
    IMG_SIZE = 50
    LR = 1e-3
    MODEL_NAME = f'dogsvscats-{LR}-CNN.model'
    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    TESTING = "PetImages/Testing"
    LABELS = {CATS: 0, DOGS: 1}

    training_data = []

    def make_training_data(self):
        for label in self.LABELS:
            for f in os.listdir(label):
                if "jpg" in f:
                    try:
                        path = os.path.join(label, f)
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
                        self.training_data.append([np.array(img), self.LABELS[label]])
                    except Exception as e:
                        print(label, f, str(e))

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)


dogsvcats = DogsVSCats()
dogsvcats.make_training_data()
print(len(dogsvcats.training_data))

training_data = np.load("training_data.npy", allow_pickle=True)
print(len(training_data))

X = np.array([i[0] for i in training_data]).reshape(-1, dogsvcats.IMG_SIZE, dogsvcats.IMG_SIZE, 1)
X = X/255.0
y = [i[1] for i in training_data]

model = Sequential()

model.add(Conv2D(32, (5, 5), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

model.add(Dense(512))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, y, batch_size=64, epochs=10, validation_split=0.3)
