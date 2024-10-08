import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Load the JSON data into a DataFrame (modify the path as per your file location)
data = pd.read_json("files/read_files/2024-10-07/AGT-2024-10-07.json")

# Convert the Timestamp to datetime for easier handling
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Select relevant columns for correlation and clustering (Temperature, Moisture, Light, Conductivity)
features = data[['Temperature', 'Moisture', 'Light', 'Conductivity']]

# Step 1: Correlation Analysis
# Calculate the correlation matrix
correlation_matrix = features.corr()

# Plot the correlation matrix in a separate window
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")

# Step 2: Clustering with K-Means
# Initialize KMeans model (using 3 clusters as an example)
kmeans = KMeans(n_clusters=3)

# Fit the model and predict the cluster for each data point
data['Cluster'] = kmeans.fit_predict(features)

# Plot clustering results in a separate window
plt.figure(figsize=(6, 4))
plt.scatter(data['Temperature'], data['Light'], c=data['Cluster'], cmap='viridis')
plt.title("K-Means Clustering")
plt.xlabel("Temperature")
plt.ylabel("Light")

# Display both figures (correlation matrix and clustering)
plt.show()
