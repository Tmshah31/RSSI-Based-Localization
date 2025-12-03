import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")

# Remove unnamed column if present
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"], errors="ignore")

# Convert to numeric just in case
data["X"] = pd.to_numeric(data["X"], errors="coerce")
data["Y"] = pd.to_numeric(data["Y"], errors="coerce")

print("len of X: ", len(data["X"]))
print("len of Y: ", len(data["Y"]))

print("Total rows:", len(data))
print("Unique coordinate pairs:", len(data[['X','Y']].drop_duplicates()))


# Access point coordinates
AP1 = (0, 0)
AP2 = (0, 17)
AP3 = (-19, 0)

plt.figure(figsize=(9, 7))

# Plot all measured points (EVERY SINGLE ONE)
plt.scatter(data["X"], data["Y"], s=18, color="blue", alpha=0.7, label="Measurement Points")

# Plot APs
plt.scatter(*AP1, color="red", s=200, marker="X", label="AP1")
plt.scatter(*AP2, color="green", s=200, marker="X", label="AP2")
plt.scatter(*AP3, color="orange", s=200, marker="X", label="AP3")

plt.title("Measurement Points + Access Point Locations")
plt.xlabel("X (tiles)")
plt.ylabel("Y (tiles)")
plt.grid(True)
plt.legend()

plt.xlim(auto=True)
plt.ylim(auto=True)


plt.show()
