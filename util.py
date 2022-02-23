import pandas as pd
import matplotlib.pyplot as plt


def preprocess():
    df = pd.read_csv('dataset_phishing.csv')

    df.drop(['url'], axis=1, inplace=True)
    df.to_csv('phishing.csv', index=False)

    print('Processing complete.')


def visualize_trainingdata(historyObj):
    # list all data in history
    #print(historyObj.history.keys())

    # summarize history for accuracy
    plt.plot(historyObj.history['accuracy'])
    plt.plot(historyObj.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(historyObj.history['loss'])
    plt.plot(historyObj.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
