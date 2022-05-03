import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, END
from tkinter import scrolledtext
from tkinter import filedialog as fd
from basic_features import BasicFeatures
from external_features import ExternalFeatures
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

url_list = []
column_names = ['num_@', 'url_length', 'host_length', 'num_.', 'num_-', 'num_?', 'num_&',
                'num_=', 'num_', 'num_~', 'num_%', 'num_/',
                'num_*', 'num_:', 'num_comma', 'num_;', 'num_$',
                'numSpaces', 'num_www', 'num_com', 'num_bslash', 'num_digits', 'num_params',
                'hostname_2length_ratio', 'url_entropy', 'contains_port',
                'http_in_query', 'tld_in_path', 'shortener_url', 'is_ip', 'url_length_sus', 'sus_extension_type',
                'phish_hints', 'count_fragment', 'months_since_creation',
                'months_since_expired', 'url_is_live', 'num_redirects', 'body_length', 'numLinks',
                'numImages', 'script_length', 'specialCharacters', 'scriptBodyRatio', 'open_page_rank', 'is_https']


### Used for preparing csv data to be used with keras
def preprocess():
    df = pd.read_csv('data/b.csv')

    df.drop(['url'], axis=1, inplace=True)
    df.to_csv('data/b1.csv', index=False)

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
def get_save_location():
    default_extension = '.csv'
    filename = fd.asksaveasfilename(filetypes=(('csv file', '.csv'),))

    if '.csv' in filename:
        filename = filename
        write_csv(filename, url_list)
    if '.csv' not in filename:
        filename = filename + default_extension
        write_csv(filename, url_list)


### Used to obtain feature set from an url.
def build_dataset(url):
    # basic features
    features_list = []

    basicfeatures = BasicFeatures(url)
    for i in basicfeatures.build():
        features_list.append(i)

    externalfeatures = ExternalFeatures(url)
    for i in externalfeatures.build():
        features_list.append(i)

    return features_list


def insertUpdate(url_count, url_length):
    text_output.insert(END, str(url_count) + ' URLs analyzed out of ' + str(url_length) + '.' + '\n')
    root.update()
    text_output.see(END)


### Writes feature set of url to csv file.
def write_csv(filename, url_list):
    count = 0
    numUrls = len(url_list)
    text_output.delete("1.0", "end")
    with open(filename, 'w') as write_obj:
        for i in range(len(column_names)):
            try:
                if i == len(column_names) - 1:
                    write_obj.write(str(column_names[i]) + '\n')
                else:
                    write_obj.write(str(column_names[i]) + ',')
            except IndexError:
                write_obj.write(str(column_names[i]) + '\n')
        for i in url_list:
            temp = build_dataset(i)
            count = count + 1
            print((str(count) + ' URLs analyzed out of ' + str(numUrls) + '.'))
            insertUpdate(count, numUrls)
            for x in range(len(temp)):
                try:
                    # if temp[0].count(',') > 0:
                    #   temp[0] = temp[0].replace(',', '(COMMA)')
                    if x == len(temp) - 1:
                        write_obj.write(str(temp[x]) + '\n')
                    else:
                        write_obj.write(str(temp[x]) + ',')
                except IndexError:
                    write_obj.write(str(temp[x]) + '\n')
    write_obj.close()
    print('Dataset built.')


def get_url():
    url = ''
    url = url_input.get('1.0', 'end-1c')
    return url


# Take user URL, turn into feature set, and analyze with saved model.
def analyze_url():
    # load model
    filename = "model/rf_model.joblib"
    rf_model = joblib.load(filename)


    url = get_url()
    features = build_dataset(url)

    count = 0
    for x in features:
        print(str(column_names[count]) + " " + str(features[count]))
        count = count + 1

    test = pd.DataFrame(features).replace(True, 1).replace(False, 0).to_numpy().reshape(-1, 46)

    prediction = rf_model.predict(test)

    print('Model prediction: ' + str(prediction))
    #tk.Label(tab1, text='Model confidence is: ' + str(accuracy), font=('Times New Roman', 15)).grid(column=0, row=5)

    if prediction == 0:
        text_outputTab1.insert(END, url + ' is not malicious.' + "\n", 'success')
    else:
        text_outputTab1.insert(END, url + ' is malicious.' + "\n", 'warning')


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

url_input = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, height=5, width=75, font=("Times New Roman", 15))

url_input.grid(column=0, row=3, pady=10, padx=10)

checkURLButton = tk.Button(tab1, height=2, width=25, text='Analyze URL.', command=lambda: analyze_url())
checkURLButton.grid(column=0, row=4, padx=10, pady=10)

text_outputTab1 = scrolledtext.ScrolledText(tab1, wrap=tk.WORD,
                                            width=75, height=10,
                                            bg="light grey",
                                            font=("Times New Roman", 15))

text_outputTab1.tag_config('warning', background="light grey", foreground="red")
text_outputTab1.tag_config('success', background="light grey", foreground="green")

text_outputTab1.grid(column=0, row=6, pady=10, padx=10)

################################### Tab 2 - Build Dataset Tab
ttk.Label(tab2, text="Turn URL List into dataset of URL features.",
          font=("Times New Roman", 15)).grid(column=0, row=0, pady=3)
ttk.Label(tab2, text="See README file for more information.",
          font=("Times New Roman", 15)).grid(column=0, row=1, pady=3)

text_input = scrolledtext.ScrolledText(tab2, wrap=tk.WORD,
                                       width=75, height=3,
                                       font=("Times New Roman", 15))

text_input.grid(column=0, row=3, pady=10, padx=10)

text_output = scrolledtext.ScrolledText(tab2, wrap=tk.WORD,
                                        width=75, height=10,
                                        bg="light grey",
                                        font=("Times New Roman", 15))

text_output.grid(column=0, row=6, pady=10, padx=10)

url_list_location_button = tk.Button(tab2, height=3,
                                     width=50,
                                     text="Open URL List",
                                     command=lambda: get_urllist_file_path())

url_list_location_button.grid(column=0, row=2, pady=10, padx=10)

save_location_button = tk.Button(tab2, height=3,
                                 width=50,
                                 text="Select Save Location For Features",
                                 command=lambda: get_save_location())

save_location_button.grid(column=0, row=4, pady=10, padx=10)

text_input.focus()

###Ending GUI code
# placing cursor in text area
root.eval('tk::PlaceWindow . center')
root.mainloop()
