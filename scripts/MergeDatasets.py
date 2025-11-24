import pandas as pd
import pathlib as path


def Merge_Datasets():


    df_AP1 = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/Nov20/ESP_Beacon_one_2025-11-20_09-13-42_dataset.csv")
    df_AP2 = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/Nov20/ESP_Beacon_two_2025-11-20_09-13-42_dataset.csv")
    df_AP3 = pd.read_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/Nov20/ESP_Beacon_three_2025-11-20_09-13-42_dataset.csv")

    df_AP1 = df_AP1.rename(columns={"RSSI (avg)":"RSSI_AP1"})
    df_AP2 = df_AP2.rename(columns={"RSSI (avg)":"RSSI_AP2"})
    df_AP3 = df_AP3.rename(columns={"RSSI (avg)":"RSSI_AP3"})


    merged = df_AP1.merge(df_AP2, on=["X", "Y"])
    merged = merged.merge(df_AP3, on=["X", "Y"])


    merged = merged[["X", "Y", "RSSI_AP1", "RSSI_AP2", "RSSI_AP3"]]

    merged.to_csv("/home/tmshah/RSSI_Localization/RSSI-Based-Localization/data/")

if __name__ == "__main__":
    Merge_Datasets()