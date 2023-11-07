import pandas as pd
import glob
import os

class CSVReducer:
    def __init__(self, main_roads_path, data_path, path_to_save):
        self.data_path = data_path
        self.main_roads_path = main_roads_path
        self.data_path_to_save = path_to_save
        self.df = None
        self.main_roads_df = None
        self.street_names = {
        "Ponte Vasco da Gama": [3651, 3629],
        "A36": [3563, 3564, 3565],
        "IC16": [3680, 3681, 3662, 3663],
        "N117": [933, 934, 990],
        "Marginal": [75, 76, 106],
        "IC2 (Sacavém)": [3736, 3728],
        "A1": [3524, 3564],
        "Calcada De Carriche": [3460, 3500, 3501],
        "IC19": [1758, 1759, 1699, 1698],
        "A5": [757, 758],
        "Ponte 25 Abril 102/103": [102, 103],
        "A16" : [2656, 2594],
        # "Terminal Fluvial do Cais Do Sodre": [303, 304],
        # "Terrerio do Paco - Terminal Fluvial": [356, 357,358],
        }
        os.makedirs(self.data_path_to_save, exist_ok=True)

    def read(self):
        self.main_roads_df = pd.read_csv(self.main_roads_path, low_memory=False)

    def reduce(self):
        self.read()
        csv_files = glob.glob(os.path.join(self.data_path, "*.csv"))
        for file in csv_files:
            self.df = pd.read_csv(file, low_memory=False)
            self.df = self.df[self.df["Grid_ID"].isin(self.main_roads_df["id"])]
            self.df = self.df.sort_values(by=['Grid_ID'])
            self.save_csv(os.path.join(self.data_path_to_save, os.path.basename(file)))

    def save_csv(self, path):
        base, ext = os.path.splitext(path)
        new_path = f"{base}_reduced{ext}"
        self.df.to_csv(new_path, index=False)