import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score
import torch
from nn import SoilHealthPredictor

def visualize(y_test, test_predictions, y_train, X_train, model):
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

    # Plot actual vs predicted values for the training and test sets
    plt.scatter(y_train.numpy(),
                model(X_train).detach().numpy(),
                color='blue',
                label='Training Data')
    plt.scatter(y_test.numpy(),
                model(X_test).detach().numpy(),
                color='red',
                label='Test Data')

    # Plot the line of perfect predictions
    max_val = max(np.max(y_train.numpy()), np.max(y_test.numpy()))
    plt.plot([0, max_val], [0, max_val],
             color='black',
             label='Perfect Predictions')

    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted Values')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Load the saved data
    y_test = torch.tensor(np.load('y_test.npy'))
    test_predictions = torch.tensor(np.load('test_predictions.npy'))
    y_train = torch.tensor(np.load('y_train.npy'))
    X_train = torch.tensor(np.load('X_train.npy'))

    # Load the saved model
    model = SoilHealthPredictor()
    model.load_state_dict(torch.load('trained_model.pth'))
    model.eval()

    # Call the visualize function
    visualize(y_test, test_predictions, y_train, X_train, model)
