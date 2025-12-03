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
# z-score normalize all RSSI values so every AP can be used
scaler = StandardScaler()
x = scaler.fit_transform(data[["RSSI_AP1", "RSSI_AP2", "RSSI_AP3"]])



# classify Y -> labels 
y = data[["X", "Y"]].values



def distance(x,y):
    # return np.sqrt(np.sum((x-y)**2))
    return np.sum(np.abs(x - y))    # Use Manhatten distance more helpful with outliers and a grid like environment



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
        print(f"    ----------K={self.k}----------")

        #multiply by 0.2921 to get meters from 11.5 inches
        print(f"Mean error:{np.mean(errors)*0.2921} m")
        print(f"Median error:{np.median(errors)*0.2921} m")
        print(f"80% Percentile: {np.percentile(errors, 80)*0.2921} m")
        print(f"Maximum erorrs: {np.max(errors)*0.2921} m")

        return np.mean(errors)*0.2921, np.median(errors)*0.2921


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



def plot_error(prediction, y_test, k):
    # ERROR VECTOR (PLOT AROUND ZERO)
    error_vectors = prediction - y_test   # (N, 2) array

    plt.figure(figsize=(6,6))
    plt.scatter(error_vectors[:,0], error_vectors[:,1], alpha=0.7)

    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    plt.xlabel("Error in X (tiles)")
    plt.ylabel("Error in Y (tiles)")
    plt.title(f"Localization Error Distribution Around Zero (K = {k})")
    plt.grid(True)
    plt.gca().set_aspect('equal', 'box')
    plt.show()


if __name__ == "__main__":

    k_3 = 3
    k_5 = 5
    k_7 = 7

    # split current dataset into training and test (Record new values for test?)
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.10, random_state=2)

    # ------------------------------ k = 3 ------------------------------
    knn_3 = KNN_RSSI(k_3)
    knn_3.fit(x_train, y_train)
    prediction_3 = knn_3.prediction(x_test)

    # mean square error
    errors_3 = np.sqrt(np.sum((prediction_3 - y_test)**2, axis=1))

    #plot_error(prediction_3, y_test, k_3)

    # ------------------------------ k = 5 ------------------------------
    knn_5 = KNN_RSSI(k_5)
    knn_5.fit(x_train, y_train)
    prediction_5 = knn_5.prediction(x_test)

    # mean square error
    errors_5 = np.sqrt(np.sum((prediction_5 - y_test)**2, axis=1))

    #plot_error(prediction_5, y_test, k_5)


    # ------------------------------ k = 7 ------------------------------
    knn_7 = KNN_RSSI(k_7)
    knn_7.fit(x_train, y_train)
    prediction_7 = knn_7.prediction(x_test)

    # mean square error
    errors_7 = np.sqrt(np.sum((prediction_7 - y_test)**2, axis=1))

    #plot_error(prediction_7, y_test, k_7)



    mean_3, median_3 = knn_3.error_print(errors_3)
    mean_5, median_5 = knn_5.error_print(errors_5)
    mean_7, median_7 = knn_7.error_print(errors_7)

    x_axis = [1,3,5]
    average = [mean_3, mean_5, mean_7]
    median = [median_3, median_5, median_7]

    colors = ["red", "green", "blue"]  

    plt.figure(figsize=(8,6))
    for k, val, c in zip(x_axis, average, colors):
        plt.scatter(k, val, color=c, s=80, label=f"K = {k}")

    plt.plot(x_axis, average, color="black", linewidth=1)
    plt.title("Mean Error vs K Value")
    plt.xlabel("K value")
    plt.ylabel("Mean Error (m)")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(8,6))
    for k, val, c in zip(x_axis, median, colors):
        plt.scatter(k, val, color=c, s=80, label=f"K = {k}")

    plt.plot(x_axis, median, color="black", linewidth=1)  # optional connecting line

    plt.title("Median Error vs K Value")
    plt.xlabel("K value")
    plt.ylabel("Median Error (m)")
    plt.grid(True)
    plt.legend()
    plt.show()


    #knn.visualize_neighbors(x_train, y_train, x_test, y_test)


