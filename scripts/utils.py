import pandas as pd
import os

def load_dataset():
    DATA_PATH = os.path.join("../data", "Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv")
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df
    else:
        print(f"Dataset not found at {DATA_PATH}")
        return None
