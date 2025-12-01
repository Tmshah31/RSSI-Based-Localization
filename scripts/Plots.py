import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

data = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/MergedDataset.csv")

# Drop extra column
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"], errors="ignore")

# Convert tile coords → floats
data["X"] = pd.to_numeric(data["X"], errors="coerce")
data["Y"] = pd.to_numeric(data["Y"], errors="coerce")


AP1 = (0, 0)
AP2 = (0, 17)
AP3 = (-19, 0)


# Create a grid
grid_x, grid_y = np.mgrid[
    data["X"].min():data["X"].max():200j,
    data["Y"].min():data["Y"].max():200j
]

# Each measurement point contributes a "1"
values = np.ones(len(data))

# Interpolate to create a smooth coverage map
coverage = griddata(
    (data["X"], data["Y"]),
    values,
    (grid_x, grid_y),
    method="nearest",
    fill_value=0
)


plt.figure(figsize=(8, 7))

# Shaded region
plt.imshow(
    coverage.T,
    extent=(data["X"].min(), data["X"].max(), data["Y"].min(), data["Y"].max()),
    origin="lower",
    cmap="Greys",
    alpha=0.35  # transparency
)

# Plot measurement points
plt.scatter(data["X"], data["Y"], s=20, color="blue", alpha=0.45, label="Sampled Points")

# Plot AP Locations
plt.scatter(*AP1, color="red", marker=".", s=200, label="AP1")
plt.scatter(*AP2, color="green", marker=".", s=200, label="AP2")
plt.scatter(*AP3, color="orange", marker=".", s=200, label="AP3")

# Labels & Formatting
plt.xlabel("X (tiles)")
plt.ylabel("Y (tiles)")
plt.title("Measurement Coverage + AP Locations")
plt.grid(True)
plt.legend()
plt.xlim([-20,7])
plt.ylim([-9,26])
plt.show()
