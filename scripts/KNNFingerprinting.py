from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#load dataset
data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")
data = data.drop(columns = ["Unnamed: 0"])

data["RSSI_AP1"] = pd.to_numeric(data["RSSI_AP1"], errors="coerce")
data["RSSI_AP2"] = pd.to_numeric(data["RSSI_AP2"], errors="coerce")
data["RSSI_AP3"] = pd.to_numeric(data["RSSI_AP3"], errors="coerce")





# classify X -> parameters
x = data[["RSSI_AP1", "RSSI_AP2"]].values



# # # classify Y -> labels 
y = data[["X", "Y"]].values


# # #split current dataset into training and test (Record new values for test?)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.20, random_state=2)



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

        weights = 1 / (d + 1e-6)

        predicted = np.sum(coordinates * weights[:,None], axis = 0) / np.sum(weights)

        return predicted


        # labels = np.array([self.y_train[i] for i in nearest_indeces])

        # compute = labels.mean(axis = 0)

        # return compute





knn = KNN_RSSI(11)
knn.fit(x_train, y_train)
prediction = knn.prediction(x_test)
errors = np.sqrt(np.sum((prediction - y_test)**2, axis=1))

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


