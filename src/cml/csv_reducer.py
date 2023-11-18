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

    def save_csv(self, path, suffix="_reduced"):
        base, ext = os.path.splitext(path)
        new_path = f"{base}{suffix}{ext}"
        self.df.to_csv(new_path, index=False)

    def interpolate_data(self):
        csv_files = glob.glob(os.path.join(self.data_path, "*.csv"))
        for file in csv_files:
            self.df = pd.read_csv(file, low_memory=False)
            self.df = self.df.interpolate(method='linear', limit_direction='forward', axis=0)
            for col in self.df.columns:
                if self.df[col].dropna().apply(float.is_integer).all():  # Check if all non-NaN values are integers
                    self.df[col] = self.df[col].astype(int)
            self.save_csv(os.path.join(self.data_path_to_save, os.path.basename(file)), "_interpolated")