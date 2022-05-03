import keras.layers.core
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import matplotlib.pyplot as plt
import build_dataset
import util as util

dataset = np.loadtxt('data/allurls_test1.csv', delimiter=',', skiprows=1)

# split into input (X) and output (Y) variables
X = dataset[:, 0:46]
Y = dataset[:, 46]

# construct model
model = Sequential()
model.add(Dense(24, input_dim=46, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X, Y, validation_split=0.10, epochs=50, batch_size=32)

_, accuracy = model.evaluate(X)
print('Accuracy:: %.2f' % (accuracy * 100))

util.visualize_trainingdata(history)

modelsave = input('Save this model? Y/N')

if modelsave == "Y":
    # serialize model to json and save weights
    model_json = model.to_json()
    with open('model/model.json', 'w') as json_file:
        json_file.write(model_json)
        print('Serialized model saved.')
        json_file.close()

    model.save_weights('model/model_weights.h5')
    print('Saved model weights.')
else:
    print('Done')
