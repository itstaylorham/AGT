import json
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# Prepare train data for input
with open('sesh.json', 'r') as f:
    input_data = json.load(f)

samples = []
for d in input_data:
    row = [d['Light'], d['Moisture'], d['Temperature'], d['Conductivity'], d['Class']]
    samples.append(row)

train_df = pd.DataFrame(samples, columns=['Light', 'Moisture', 'Temperature', 'Conductivity', 'Class'])

# Define input and output variables
X = train_df[['Light', 'Moisture', 'Temperature', 'Conductivity']]
y = train_df['Class']

# Fit logistic regression model
model = sm.Logit(y, sm.add_constant(X)).fit()

# Plot data points
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y)

# Plot decision boundary
x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:, 0].max() + 1
y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
Z = model.predict(sm.add_constant(np.c_[xx.ravel(), yy.ravel(), np.zeros(xx.ravel().shape[0]), np.zeros(xx.ravel().shape[0])]))
Z = Z.reshape(xx.shape)
plt.contour(xx, yy, Z, cmap=plt.cm.Paired)

plt.xlabel('Light')
plt.ylabel('Moisture')
plt.title('Single Layer Neural Network Decision Boundary')
plt.show()
