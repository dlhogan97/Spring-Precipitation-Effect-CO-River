import pandas as pd
import os
import subprocess

yrs = input("Type years to download (separated by space): ")
year_list = str.split(yrs,' ')

for yr in year_list:
    if os.path.exists('WY'+str(yr)+'.zip'):
        print("This year was already downloaded.")

    else:
        wrf_urls = pd.read_csv('../data/wrf_run_urls.txt',header=None, skiprows=1)[0].to_list()
        wrf_years = pd.read_csv('../data/wrf_run_urls.txt').columns
        wrf_url_dict = dict(zip(wrf_years,wrf_urls))
        desired_cmd = f"wget -O /storage/dlhogan/sos/data/WY{yr}.zip {wrf_url_dict[yr]}"
        print(desired_cmd)
        subprocess.run(desired_cmd , shell=True, check=True)