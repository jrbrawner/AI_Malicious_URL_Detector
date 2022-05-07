import pandas as pd
import numpy as np
import joblib
import pydot
from sklearn.tree import export_graphviz
import gui as gui
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
import time

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

dataset = pd.read_csv('data/url_features.csv')

# split into input (X) and output (Y) variables
inputs = dataset.iloc[:, 0:46].values
output = dataset.iloc[:, 46].values

# split into training and testing data
input_train, input_test, output_train, output_test = train_test_split(inputs, output, test_size=0.10, random_state=0)

# scale values
sc = StandardScaler()
input_train = sc.fit_transform(input_train)
input_test = sc.transform(input_test)
# construct model
rf = RandomForestClassifier(n_estimators=100, random_state=0, verbose=1)
rf.fit(input_train, output_train)
output_pred = rf.predict(input_test)
# print results
print(confusion_matrix(output_test, output_pred))
print(classification_report(output_test, output_pred))
print(accuracy_score(output_test, output_pred))
# Get numerical feature importance
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(dataset, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]


modelsave = input('Save this model? Y/N')

if modelsave == "Y" or modelsave == "y":
    # save model as pickle file
    filename = "model/rf_model.joblib"
    joblib.dump(rf, filename)


graph_pic = input('Save picture of rf tree? Y/N')


if graph_pic == "Y" or graph_pic == 'y':
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file='model/tree.dot', feature_names=gui.column_names, rounded=True, precision=1)
    # Use dot file to create a graph
    (graph,) = pydot.graph_from_dot_file('model/tree.dot')
    # Write graph to a png file
    graph.write_png('model/tree.png')

visualize = input('Visualize feature importance? Y/N')

if visualize == 'Y' or visualize == 'y':
    start_time = time.time()
    result = permutation_importance(
        rf, input_test, output_test, n_repeats=10, random_state=0
    )
    elapsed_time = time.time() - start_time
    print(f"Elapsed time to compute the importance: {elapsed_time:.3f} seconds")

    forest_importances = pd.Series(result.importances_mean, index=gui.column_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importance using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()
    print('Done')
else:
    print('Done')




