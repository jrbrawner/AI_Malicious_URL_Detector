import pandas as pd

df = pd.read_csv('dataset_phishing.csv')

df.drop(['url'], axis = 1, inplace=True)
df.to_csv('phishing.csv', index=False)

print('Processing complete.')
