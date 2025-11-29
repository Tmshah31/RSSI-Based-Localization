import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# LOAD MERGED DATASET
data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")

# Keep only AP1 + AP2
data = data[['X','Y','RSSI_AP1','RSSI_AP2']].dropna()

# Convert to numpy arrays
X = data[['RSSI_AP1','RSSI_AP2']].values
Y = data[['X','Y']].values

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=3)

# Distance function
def dist(a, b):
    return np.sqrt(np.sum((a - b)**2))

# Weighted KNN predictor
def predict_knn(rssi, x_train, y_train, k=7):
    distances = np.array([dist(rssi, pt) for pt in x_train])
    idx = np.argsort(distances)[:k]

    coords = y_train[idx]
    d = distances[idx]
    w = 1/(d + 1e-6)

    pred = np.sum(coords * w[:,None], axis=0) / np.sum(w)
    return pred, idx

# PICK RANDOM TEST POINT
rand_index = np.random.randint(0, len(x_test))
test_RSSI = x_test[rand_index]
actual_xy = y_test[rand_index]

pred_xy, neighbor_idx = predict_knn(test_RSSI, x_train, y_train, k=3)

# Compute error
error_tiles = np.sqrt(np.sum((pred_xy - actual_xy)**2))
error_meters = error_tiles * 0.2921

print("\n--- Random Test Point Evaluation ---")
print("Test RSSI:", test_RSSI)
print("Actual XY:", actual_xy)
print("Predicted XY:", pred_xy)
print(f"Error: {error_tiles:.3f} tiles ({error_meters:.3f} meters)")

# PLOT RSSI FEATURE SPACE
plt.figure(figsize=(7,6))

# Plot dataset fingerprints
plt.scatter(x_train[:,0], x_train[:,1], color='black', alpha=0.5, label="Training fingerprints")

# Highlight neighbors
nn_points = x_train[neighbor_idx]
plt.scatter(nn_points[:,0], nn_points[:,1], s=120, edgecolors='green',
            facecolors='none', linewidths=2, label="K nearest neighbors")

# Plot test RSSI point
plt.scatter(test_RSSI[0], test_RSSI[1], color='red', s=120, label="Test RSSI point")

plt.xlabel("RSSI from AP1 (dBm)")
plt.ylabel("RSSI from AP2 (dBm)")
plt.title("KNN in RSSI Feature Space (AP1 vs AP2)")
plt.legend()
plt.grid(True)
plt.show()
