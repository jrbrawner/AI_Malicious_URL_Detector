import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import util as util

dataset = np.loadtxt('phishing.csv', delimiter=',', skiprows=1)

# split into input (X) and output (Y) variables
X = dataset[:, 0:87]
Y = dataset[:, 87]

model = Sequential()
model.add(Dense(12, input_dim=87, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X, Y, validation_split=0.40, epochs=150, batch_size=32)

_, accuracy = model.evaluate(X, Y)
print('Accuracy:: %.2f' % (accuracy * 100))

predictions = (model.predict(X) > 0.5).astype(int)

# for i in range(5):
#   print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], Y[i]))

util.visualize_trainingdata(history)
