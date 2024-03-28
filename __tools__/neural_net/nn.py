import torch
import json
import torch.nn as nn
import numpy as np
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

print('Testing neural net file...')
# Build input, hidden and output layers with PyTorch
class SoilHealthPredictor(nn.Module):

    def __init__(self):
        super(SoilHealthPredictor, self).__init__()
        self.layer1 = nn.Linear(4, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 16)
        self.layer4 = nn.Linear(16, 4)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = torch.relu(self.layer3(x))
        x = self.layer4(x)
        return x

model = SoilHealthPredictor()

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Load spider plant ideal dataset
ideal_data = []
for i in range(1, 10):
    with open(
            f'__files__/read_files/2023-04-{i:02d}/AGT-2023-04-{i:02d}.json',
            'r') as f:
        day_data = json.load(f)
        ideal_data.extend(day_data)

# Extract features and normalize
features = []
targets = []

for entry in ideal_data:
    features.append([
        entry["Light"], entry["Moisture"], entry["Conductivity"],
        entry["Temperature"]
    ])
    targets.append([
        entry["Temperature"], entry["Moisture"], entry["Light"],
        entry["Conductivity"]
    ])

scaler = StandardScaler()
features = scaler.fit_transform(features)

# Set the random seed for PyTorch
torch.manual_seed(20)

# Set the random seed for NumPy
np.random.seed(20)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    targets,
                                                    test_size=0.2,
                                                    random_state=20
)


X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# Training parameters
epochs = 100
batch_size = 32

# Training loop
for epoch in range(epochs):
    for i in range(0, len(X_train), batch_size):
        # Get mini-batch
        inputs = X_train[i:i + batch_size]
        labels = y_train[i:i + batch_size]

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Calculate training and test losses
    with torch.no_grad():
        train_loss = criterion(model(X_train), y_train)
        test_loss = criterion(model(X_test), y_test)
    
    # Print losses
    print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')

with torch.no_grad():
    test_predictions = model(X_test)

actual_temperatures = y_test[:, 0].numpy()
predicted_temperatures = test_predictions[:, 0].numpy()

# Calculate the R2 score for temperature predictions
temperature_r2_score = r2_score(actual_temperatures, predicted_temperatures)

# Normalize the R2 score to scale 0 to 100
health_score = temperature_r2_score * 100
health_score = max(0, health_score)

# Calculate the R2 score (correlation) between the predicted and actual targets for the test set
test_correlation = r2_score(y_test.numpy(), test_predictions.numpy(), multioutput='uniform_average')


# Normalize the R2 score to scale 0 to 100
health_score = temperature_r2_score * 100
test_correlation = r2_score(y_test.numpy(), test_predictions.numpy(), multioutput='uniform_average')


health_score = max(0, health_score)


from sklearn.metrics import r2_score

temperature_r2_score = r2_score(actual_temperatures, predicted_temperatures)


from sklearn.metrics import r2_score

temperature_r2_score = r2_score(actual_temperatures, predicted_temperatures)



with torch.no_grad():
    test_predictions = model(X_test)

# Create a 3D scatter plot with the actual and predicted values
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot actual data
ax.scatter(y_test[:, 0], y_test[:, 1], y_test[:, 2], color='blue', label='Actual')
# Plot predicted data
ax.scatter(test_predictions[:, 0], test_predictions[:, 1], test_predictions[:, 2], color='red', label='Predicted')

ax.set_xlabel('Temperature')
ax.set_ylabel('Moisture')
ax.set_zlabel('Light')
ax.legend()
plt.show()
# Calculate the R2 score (correlation) between the predicted and actual targets for the test set
test_correlation = r2_score(y_test.numpy(), test_predictions.numpy(), multioutput='uniform_average')\

# Create a dataframe with the actual and predicted values
actual_df = pd.DataFrame(y_test.numpy(), columns=['Temperature (Actual)', 'Moisture (Actual)', 'Light (Actual)', 'Conductivity (Actual)'])
predicted_df = pd.DataFrame(test_predictions.numpy(), columns=['Temperature (Predicted)', 'Moisture (Predicted)', 'Light (Predicted)', 'Conductivity (Predicted)'])

# Combine actual and predicted dataframes
combined_df = pd.concat([actual_df, predicted_df], axis=1)

# Create scatter plot matrix using Seaborn
sns.set(font_scale=0.7)
sns.pairplot(combined_df, diag_kind=None)
plt.show()

# Plot actual data
ax.scatter(y_test[:, 0], y_test[:, 1], y_test[:, 2], color='blue', label='Actual')

# Plot predicted data
ax.scatter(test_predictions[:, 0], test_predictions[:, 1], test_predictions[:, 2], color='red', label='Predicted')

ax.set_xlabel('Temperature')
ax.set_ylabel('Moisture')
ax.set_zlabel('Light')
ax.legend()
plt.show()

# Plotting the actual vs predicted values for the training set
plt.scatter(y_train.numpy(),
            model(X_train).detach().numpy(),
            color='blue',
            label='Training Data')
plt.scatter(y_test.numpy(),
            model(X_test).detach().numpy(),
            color='red',
            label='Test Data')

# Plotting the line of perfect predictions
max_val = max(np.max(y_train.numpy()), np.max(y_test.numpy()))
plt.plot([0, max_val], [0, max_val],
         color='black',
         label='Perfect Predictions')

plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values')
plt.legend()
plt.show()

print(
    f'\nFinal R2 Score (Correlation) for the Test Set: {test_correlation:.4f}')
print(f'Temperature Health Score: {health_score:.2f}')
