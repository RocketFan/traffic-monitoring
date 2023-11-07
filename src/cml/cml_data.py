import pandas as pd
import glob
import os

class CMLData:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def read(self):
        csv_files = glob.glob(os.path.join(self.dir_path, '*.csv'))
        dfs = []

        for csv_file in csv_files:
            df = pd.read_csv(csv_file, dtype={'D1': 'string', 'E6': 'string'})
            dfs.append(df)

    def rename_columns(self, df):
        df.rename(columns={'D1': 'id', 'E6': 'name'}, inplace=True)
        return df 