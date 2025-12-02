from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#load dataset
data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")
data = data.drop(columns = ["Unnamed: 0"])

#convert the RSSI values to floats
data["RSSI_AP1"] = pd.to_numeric(data["RSSI_AP1"], errors="coerce")
data["RSSI_AP2"] = pd.to_numeric(data["RSSI_AP2"], errors="coerce")
data["RSSI_AP3"] = pd.to_numeric(data["RSSI_AP3"], errors="coerce")


# classify X -> parameters
# Normalize all RSSI values so every AP can be used
scaler = StandardScaler()
x = scaler.fit_transform(data[["RSSI_AP1", "RSSI_AP2", "RSSI_AP3"]])



# classify Y -> labels 
y = data[["X", "Y"]].values



def distance(x,y):
    # return np.sqrt(np.sum((x-y)**2))
    return np.sum(np.abs(x - y))    # Use Manhatten distance more helpful with outliers



#Class KNN
class KNN_RSSI:

    def __init__(self,k):
        self.k = k

    def fit(self, x, y):
        self.x_train = x
        self.y_train = y


    def prediction(self, RSSI_list):
        predictions = [self.predictor(RSSI) for RSSI in RSSI_list]

        return np.array(predictions)
    

    def predictor(self,RSSI):
        distances = np.array([distance(point, RSSI) for point in self.x_train])

        nearest_indices = np.argsort(distances)[:self.k]

        coordinates = np.array([self.y_train[i] for i in nearest_indices])

        d = distances[nearest_indices]


        # compute the weights per the APs (avoid division by zero) -> more distance means the AP has less power
        weights = 1 / (d + 1e-6)

        predicted = np.sum(coordinates * weights[:,None], axis = 0) / np.sum(weights)

        return predicted
    
    def locate_point(self, rssi1, rssi2, rssi3):
        
        RSSI_arr = np.array([rssi1, rssi2, rssi3])

        return self.predictor(RSSI_arr)
    

    def error_print(self, errors):
        print(f"----------K={self.k}----------")
        print(f"Mean error:{np.mean(errors)*0.2921} m")
        print(f"Median error:{np.median(errors)*0.2921} m")
        print(f"80% Percentile: {np.percentile(errors, 80)*0.2921} m")
        print(f"Maximum erorrs: {np.max(errors)*0.2921} m")

    def visualize_neighbors(self, x_train, y_train, x_test, y_test):

        # Pick random test sample
        idx = np.random.randint(0, len(x_test))
        test_rssi = x_test[idx]
        actual_xy = y_test[idx]

        # Compute nearest neighbors
        distances = np.array([distance(point, test_rssi) for point in x_train])
        n_idx = np.argsort(distances)[:self.k]

        pred_xy = self.predictor(test_rssi)

        # Plot RSSI Feature Space
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_subplot(111, projection = '3d')


        ax.scatter(x_train[:, 0], x_train[:, 1], x_train[:,2], alpha=0.5, label="Training Data")

        # Neighbors circled
        ax.scatter(x_train[n_idx, 0], x_train[n_idx, 1], x_train[n_idx, 2],
                    edgecolors="green", facecolors="none", s=200, linewidths=2,
                    label="Nearest Neighbors")

        # Test RSSI
        ax.scatter(test_rssi[0], test_rssi[1], test_rssi[2], color="red", s=120, label="Test RSSI")

        ax.set_xlabel("RSSI_AP1 (dBm)")
        ax.set_ylabel("RSSI_AP2 (dBm)")
        ax.set_zlabel("RSSI_AP3 (dBm)")
        ax.set_title("AP1 vs AP2")
        ax.legend()
        ax.grid(True)
        plt.show()

        print("Neighbor Visualization:")
        print("Test RSSI:", test_rssi)
        print("Actual XY:", actual_xy)
        print("Predicted XY:", pred_xy)
        print("Error (tiles):", np.sqrt(np.sum((pred_xy - actual_xy)**2)))
        print("Error (meters):", np.sqrt(np.sum((pred_xy - actual_xy)**2))*0.2921)




if __name__ == "__main__":

    # split current dataset into training and test (Record new values for test?)
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.10, random_state=2)

    knn = KNN_RSSI(7)
    knn.fit(x_train, y_train)
    prediction = knn.prediction(x_test)
    errors = np.sqrt(np.sum((prediction - y_test)**2, axis=1))

    #multiply by 0.2921 to get meters from 11.5 inches

    knn.error_print(errors)


    #visualize predicted and actual
    plt.figure(figsize = (6,6))
    plt.title("Actual vs Predicted Coordinated (K=7)")
    plt.scatter(y_test[:,0], y_test[:,1], label = "Actual", alpha = 0.8)
    plt.scatter(prediction[:,0], prediction[:,1], label = "Predicted", alpha = 0.8)
    plt.xlabel("X Coord")
    plt.ylabel("Y Coord")
    plt.legend()
    plt.grid(True)
    plt.show()

    # knn.visualize_neighbors(x_train, y_train, x_test, y_test)


