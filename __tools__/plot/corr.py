import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load the df from a JSON file into a pandas dfFrame
df = pd.read_json("sesh.json")

# convert the df types of the columns to float
df['Moisture'] = df['Moisture'].str[0]
df['Light'] = df['Light'].str[0]
df['Temperature'] = df['Temperature'].str[0]
df['Conductivity'] = df['Conductivity'].str[0]

# calculate the Pearson correlation coefficient between light and temperature
correlation = df.corr(numeric_only=True)

sns.heatmap(correlation, annot=True, cmap='YlGnBu')

print(correlation)
plt.show()


