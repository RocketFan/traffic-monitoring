import pandas as pd
import glob
import os

class VodafoneData:
    def __init__(self):
        self.trash_columns = ['Unnamed: 0', 'Unnamed: 0.1', 'extract_year', 'extract_month', 'extract_day', 'extract_year_2', 'extract_month_3', 'extract_day_4']

    def read(self, dir_path):
        csv_files = glob.glob(os.path.join(dir_path, '*.csv'))
        dfs = []

        for csv_file in csv_files:
            df = pd.read_csv(csv_file, dtype={'D1': 'string', 'E6': 'string'})
            dfs.append(df)
        
        df = pd.concat(dfs, axis=0, ignore_index=True)
        return df
    
    def preprocess(self, df):
        self.clean(df)
        self.convert_to_datetime(df)
    
    def clean(self, df):
        existing_trash_columns = [col for col in self.trash_columns if col in df.columns]
        df.drop(columns=existing_trash_columns, inplace=True)
    
    def convert_to_datetime(self, df):
        datetimes = pd.to_datetime(df['Datetime'], utc=True, errors='coerce')
        is_utc_dates = datetimes.isna()
        utc_datetimes = df[is_utc_dates]['Datetime']

        utc_datetimes = pd.to_datetime(utc_datetimes, utc=True)
        datetimes = pd.concat([datetimes[~is_utc_dates], utc_datetimes], axis=0)
        datetimes.sort_index(inplace=True)
        df['Datetime'] = datetimes