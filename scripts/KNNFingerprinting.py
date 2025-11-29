from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#load dataset
data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")
data = data.drop(columns = ["Unnamed: 0"])

#convert the RSSI values to floats
data["RSSI_AP1"] = pd.to_numeric(data["RSSI_AP1"], errors="coerce")
data["RSSI_AP2"] = pd.to_numeric(data["RSSI_AP2"], errors="coerce")
data["RSSI_AP3"] = pd.to_numeric(data["RSSI_AP3"], errors="coerce")



#attempt to remove outliers 
# data = data[
#     (data["RSSI_AP1"] > -85) & 
#     (data["RSSI_AP2"] > -85) &
#     (data["RSSI_AP3"] > -85) 
# ]

# data = data[
#     (data["RSSI_AP1"] < -40) & 
#     (data["RSSI_AP2"] < -40) &
#     (data["RSSI_AP3"] < -40) 
# ]



# for col in ["RSSI_AP1", "RSSI_AP2", "RSSI_AP3"]:
#     mean = data[col].mean()
#     std = data[col].std()
#     data[col] = (data[col] - mean) / std


# classify X -> parameters
x = data[["RSSI_AP1", "RSSI_AP2"]].values



# classify Y -> labels 
y = data[["X", "Y"]].values




# split current dataset into training and test (Record new values for test?)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.15, random_state=2)



#Eculidian distance function
def distance(x,y):
    return np.sqrt(np.sum(x-y)**2)



#Class KNN
class KNN_RSSI:

    def __init__(self,k):
        self.k = k

    def fit(self, x, y):
        self.x_train = x
        self.y_train = y


    def prediction(self, new_RSSIs):
        predictions = [self.predictor(RSSI) for RSSI in new_RSSIs]

        return np.array(predictions)
    

    def predictor(self,RSSI):
        distances = np.array([distance(point, RSSI) for point in self.x_train])

        nearest_indices = np.argsort(distances)[:self.k]

        coordinates = np.array([self.y_train[i] for i in nearest_indices])

        d = distances[nearest_indices]


        # compute the weights per the APs
        weights = 1 / (d + 1e-6)

        predicted = np.sum(coordinates * weights[:,None], axis = 0) / np.sum(weights)

        return predicted






knn = KNN_RSSI(3)
knn.fit(x_train, y_train)
prediction = knn.prediction(x_test)
errors = np.sqrt(np.sum((prediction - y_test)**2, axis=1))

# # Pick a random test index
# rand_idx = np.random.randint(0, len(x_test))
# test_rssi = x_test[rand_idx]
# actual_xy = y_test[rand_idx]

# # Use predictor to also return nearest neighbor indices
# def get_neighbors(model, RSSI):
#     distances = np.array([distance(point, RSSI) for point in model.x_train])
#     nearest_indices = np.argsort(distances)[:model.k]
#     return nearest_indices, distances

# neighbor_idx, dvals = get_neighbors(knn, test_rssi)

# # Predicted XY for the chosen point
# pred_xy = knn.predictor(test_rssi)

# # Plotting in RSSI feature space
# plt.figure(figsize=(7,6))

# # Entire fingerprint dataset
# plt.scatter(x_train[:,0], x_train[:,1], c='black', alpha=0.5, label="Training fingerprints")

# # Highlight neighbors
# plt.scatter(
#     x_train[neighbor_idx,0],
#     x_train[neighbor_idx,1],
#     s=150, edgecolors='green', facecolors='none', linewidths=2,
#     label=f"{knn.k} Nearest Neighbors"
# )

# # Test RSSI point
# plt.scatter(
#     test_rssi[0], test_rssi[1],
#     c='red', s=120, label="Test RSSI"
# )

# plt.xlabel("RSSI_AP1 (dBm)")
# plt.ylabel("RSSI_AP2 (dBm)")
# plt.title("KNN in RSSI Feature Space (AP1 vs AP2)")
# plt.legend()
# plt.grid(True)
# plt.show()

# # Print details for debugging
# print("Test RSSI:", test_rssi)
# print("Actual XY:", actual_xy)
# print("Predicted XY:", pred_xy)
# err = np.sqrt(np.sum((pred_xy - actual_xy)**2))
# print(f"Error for this sample: {err:.3f} tiles ({err*0.2921:.3f} m)")

#multiply by 0.2921 to get meters from 11.5 inches

print(f"Mean error:{np.mean(errors)*0.2921}")
print(f"Median error:{np.median(errors)*0.2921}")
print(f"80% Percentile: {np.percentile(errors, 80)*0.2921}")
print(f"Maximum erorrs: {np.max(errors)*0.2921}")


#visualize predicted and actual
plt.figure(figsize = (6,6))
plt.scatter(y_test[:,0], y_test[:,1], label = "Actual", alpha = 0.8)
plt.scatter(prediction[:,0], prediction[:,1], label = "Predicted", alpha = 0.8)
plt.xlabel("X Coord")
plt.ylabel("Y Coord")
plt.legend()
plt.grid(True)
plt.show()


