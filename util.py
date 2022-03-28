import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, END
from tkinter import scrolledtext
from tkinter import filedialog as fd
from build_dataset import *


### Used for preparing csv data to be used with keras
def preprocess():
    df = pd.read_csv('data/dataset_phishing.csv')

    df.drop(['url'], axis=1, inplace=True)
    df.to_csv('phishing.csv', index=False)

    print('Processing complete.')


### Used to display training statistics over epochs
def visualize_trainingdata(historyObj):
    # list all data in history
    # print(historyObj.history.keys())

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


### Used to get urls from txt file
def get_urllist_file_path():
    filename = fd.askopenfilename()
    text_input.insert(END, filename)

    with open(filename, 'r') as read_obj:
        for i in read_obj:
            url_list.append(i.strip())
    read_obj.close()


###Used to obtain desired filepath for built dataset
# Can be saved as csv or xlsx, csv is default
def get_save_location():
    default_extension = '.csv'
    filename = fd.asksaveasfilename(filetypes=(('csv file', '.csv'), ('excel file ', '.xlsx')))

    if '.csv' in filename:
        filename = filename
        write_csv(filename)
    if '.xlsx' in filename:
        filename = filename
        write_xlsx(filename)
    if '.csv' not in filename and '.xlsx' not in filename:
        filename = filename + default_extension
        write_csv(filename)


def write_xlsx(filename):
    pass


############################################################################################
### Code for GUI


root = tk.Tk()
root.title('AI Malicious URL Detector')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Predict URL')
tabControl.add(tab2, text='URLs to Data set')
tabControl.grid()

ttk.Label(tab1, text="Enter URL for analysis.",
          font=('Times New Roman', 15)).grid(column=0, row=0, pady=3)

url_input = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, height=3, width=50, font=("Times New Roman", 15))

url_input.grid(column=0, row=3, pady=10, padx=10)

###Tab 2
ttk.Label(tab2, text="Turn URL List into dataset of URL features.",
          font=("Times New Roman", 15)).grid(column=0, row=0, pady=3)
ttk.Label(tab2, text="See README file for more information.",
          font=("Times New Roman", 15)).grid(column=0, row=1, pady=3)

text_input = scrolledtext.ScrolledText(tab2, wrap=tk.WORD,
                                       width=50, height=3,
                                       font=("Times New Roman", 15))

text_input.grid(column=0, row=3, pady=10, padx=10)

text_output = scrolledtext.ScrolledText(tab2, wrap=tk.WORD,
                                        width=50, height=3,
                                        bg="light grey",
                                        font=("Times New Roman", 15))

text_output.grid(column=0, row=6, pady=10, padx=10)

url_list_location_button = tk.Button(tab2, height=2,
                                     width=25,
                                     text="Open URL List",
                                     command=lambda: get_urllist_file_path())

url_list_location_button.grid(column=0, row=2, pady=10, padx=10)

save_location_button = tk.Button(tab2, height=2,
                                 width=25,
                                 text="Select Save Location For Features",
                                 command=lambda: get_save_location())

save_location_button.grid(column=0, row=4, pady=10, padx=10)

text_input.focus()

###Ending GUI code
# placing cursor in text area
root.eval('tk::PlaceWindow . center')
root.mainloop()
