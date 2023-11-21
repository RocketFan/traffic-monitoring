import pandas as pd
import glob
import os
import argparse
from cml.vodafone_data import VodafoneData

class VodafoneReducer:
    def __init__(self):
        self.grids_id = []
        self.vodafone_data_helper = VodafoneData()

    def load_grids(self, grids_path):
        girds_df = pd.read_csv(grids_path, low_memory=False)
        self.grids_id = girds_df["id"].tolist()
    
    def reduce_all(self, data_path, save_path):
        csv_files = glob.glob(os.path.join(data_path, "*.csv"))
        os.makedirs(save_path, exist_ok=True)

        for file in csv_files:
            df = pd.read_csv(file, low_memory=False)
            df = self.reduce(df)
            file_path = os.path.join(save_path, os.path.basename(file))
            self.save(df, file_path)

    def reduce(self, df):
        df = df[df["Grid_ID"].isin(self.grids_id)]
        self.vodafone_data_helper.clean(df)
        df.sort_values(by=['Grid_ID', 'Datetime'], inplace=True)
        df.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
        return df

    def save(self, df, path, suffix="_reduced"):
        base, ext = os.path.splitext(path)
        new_path = f"{base}{suffix}{ext}"
        df.to_csv(new_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Reducer")
    parser.add_argument("--grids-path", required=True, help="Path to the main roads CSV file")
    parser.add_argument("--data-path", required=True, help="Path to the data CSV files")
    parser.add_argument("--save-path", default=f"{os.path.dirname(__file__)}/../data/reduced", help="Path to save the reduced CSV files")

    args = parser.parse_args()

    grids_path = args.grids_path
    data_path = args.data_path
    save_path = args.save_path
    print(grids_path, data_path, save_path)

    reducer = VodafoneReducer()
    reducer.load_grids(grids_path)
    reducer.reduce_all(data_path, save_path) 