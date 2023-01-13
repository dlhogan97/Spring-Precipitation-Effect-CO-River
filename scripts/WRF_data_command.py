import pandas as pd
import os

yr = input("Type year to download: ")

if os.path.exists('WY'+str(yr)+'.zip'):
    print("This year was already downloaded.")

else:
    wrf_urls = pd.read_csv('../data/wrf_run_urls.txt',header=None, skiprows=1)[0].to_list()
    wrf_years = pd.read_csv('../data/wrf_run_urls.txt').columns
    wrf_url_dict = dict(zip(wrf_years,wrf_urls))
    desired_cmd = f"wget -O /storage/dlhogan/sos/data/WY{yr}.zip {wrf_url_dict[yr]}"
    print(desired_cmd)