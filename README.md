# RSSI-Based Indoor Localization Using wKNN Fingerprinting

This project implements an indoor localization systems using Wi-Fi RSSI fingerprinting. The system utilizes ESP-32 microcontrollers to act as acess points and the weighted K-nearest neighbors algorithm to accurately predict a receivers indoor positioning in X-Y coordinates.

---

## Project Structure


```
RSSI-Based-Localization
|-- data
|   |-- ESP_Beacon_three_2025-11-18_13-07-13_dataset.csv
|   |-- MergedDataset.csv
|   `-- Nov20
|       |-- ESP_Beacon_one_2025-11-20_09-13-42_dataset.csv
|       |-- ESP_Beacon_three_2025-11-20_09-13-42_dataset.csv
|       `-- ESP_Beacon_two_2025-11-20_09-13-42_dataset.csv
|-- ESP_WiFi_Beacons
|   |-- include
|   |   `-- README
|   |-- lib
|   |   `-- README
|   |-- platformio.ini
|   |-- src
|   |   `-- main.cpp
|   `-- test
|       `-- README
|-- Figures
|   |-- Actual_Vs_Predicted_K3.png
|   |-- Actual_Vs_Predicted_K5.png
|   |-- Actual_Vs_Predicted_K7.png
|   |-- MeanError.png
|   `-- MedianError.png
|-- .gitignore
|-- Matlab
|   `-- HeatMap.m
|-- README.md
|-- requirements.txt
|-- RUN.sh
|-- scripts
|   |-- KNNFingerprinting.py
|   |-- MergeDatasets.py
|   |-- Plots.py
|   |-- RSSIgather_multiple.py
|   `-- RSSIgather_single.py
`-- .vscode
    |-- c_cpp_properties.json
    `-- settings.json
```

## Key Files

- **RUN.sh** - Turns on monitor mode for the specified adapter and run the python script to collect measurements 
- **requirements.txt** - File specifying all python dependencies required to successfully run the project

### **`data/`**
- **MergedDataset.csv** - Full merged dataset including RSSI measurements collected from all three APs
- **<ESPNAME_DATE>.csv** - Collections of RSSI measurements from a single AP

### **`ESP_WiFi_Beacons/`**
- **src/main.cpp** - ESP32 access point firmware code 
- **platformio.ini** - configuration file for ESP32

### **`Matlab/`**
- **HeatMap.m** - Matlab code generates a semi-interpolated heatmap of the collected RSSI values given the dataset

### **`scripts/`** 
- **KNNFingerprinting.py** - Trains and uses the wKNN model to predict the (X,Y) coordinate given RSSI measurements 
- **MergedDatasets.py** - Python script which combines all singular AP dataset into one
- **Plot.py** - Creates a grid plotting all the collected points including the AP locations
- **RSSIgather_multiple.py** - Gathers RSSI values from all three APs at once
- **RSSIgather_single.py** - Gathers RSSI values from a single selected AP


## NOTES

- Python environment not included. Must be created and activate for propoer functionality
- Code must be altered according to your specifications 
    - WLAN adapter
    - ESP32 model 
    - Dataset names