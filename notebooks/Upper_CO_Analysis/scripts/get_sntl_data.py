# This will grab relevant Snotel data for temperature, SWE, 20-inch soil moisture and preceipitation as daily values and save it as a compiled netcdf. 
# Can update with other desired features, but this script will need to be edited

import pandas as pd
import numpy as np
from datetime import datetime
import datetime as dt
import os
import json
import xarray as xr
import requests

# get soil moisture data. This provides information from the deepest sensor (20-inchs) and average temperature, but those values are skewed by surface measurements
input_string = input('Enter site_ids separated by comma: ')
print("\n")
site_ids = input_string.split(',')

filename = input('Enter name for file: ')

API_DOMAIN = "https://api.snowdata.info/"

print("\n")
# grabs input
edate = input('Type end date (format %Y%m%d): ')
edate = datetime.strptime(edate,'%Y%m%d')

def get_awdb_data(
    site_ids,
    elements=["WTEQ", "PREC"],
    sdate=datetime(1899, 10, 1),
    edate=edate,
    orient="records",
    server=API_DOMAIN,
    sesh=None,
):
    """
    Takes a list of site ids or a single site id and by default returns SWE period of record data as a single or list of dataframes,
    but user can pass args to modify data returned.
    Valid elements include WTEQ, SNWD, PREC, SMS, STO, TAVG
    site_id takes the form of a triplet made from <network_site_id>:<state_abbrv>:<network> where network is either SNTL or MNST
    """
    dfs = []
    return_single = False
    if not isinstance(site_ids, list):
        site_ids = [site_ids]
        return_single = True
    for site_id in site_ids:
        for element in elements:
            endpoint = "data/getDaily"
            date_args = f"sDate={sdate:%Y-%m-%d}&eDate={edate:%Y-%m-%d}"
            frmt_args = f"format=json&orient={orient}"
            all_args = f"?triplet={site_id}&{date_args}&element={element}&{frmt_args}"
            url = f"{server}{endpoint}{all_args}"
            print(
                f"getting data for {site_id} {element} starting {sdate:%Y-%m-%d} "
                f"and ending {edate:%Y-%m-%d}"
            )
            data_col_lbl = f"{element}"
            if sesh:
                req = sesh.get(url)
            else:
                req = requests.get(url)
            if req.ok:
                df = pd.DataFrame.from_dict(req.json())
                df.columns = [data_col_lbl,"Date"]
                df.set_index("Date", inplace=True)
            else:
                print("  No data returned!")
                df = (
                    pd.DataFrame(
                        data=[{"Date": pd.NaT, data_col_lbl: np.nan}],
                    )
                    .set_index("Date")
                    .dropna()
                )
            dfs.append(df)
        if return_single:
            return dfs[0]
    return dfs

# Grab dataframes
sntl_dfs = get_awdb_data(site_ids=site_ids)

# Make the index a datetime
for i,df in enumerate(sntl_dfs):
    df.index = pd.to_datetime(df.index)
    sntl_dfs[i] = df

# create a dictionary for conversion to xarray
sntl_df_dict = {}
for i,site in enumerate(site_ids):
    if sntl_dfs[i] is not None:
        sntl_df_dict[site] = pd.concat(sntl_dfs[i:i+2], axis=1).sort_index().to_xarray()

# convert to xarray
sntl_ds = xr.concat(sntl_df_dict.values(), pd.Index(sntl_df_dict.keys(), name='Location'))
sntl_ds = sntl_ds.assign_coords({'WY':sntl_ds.Date.dt.year.where(sntl_ds.Date.dt.month < 10, sntl_ds.Date.dt.year + 1)})

# Unit conversions

sntl_ds['WTEQ'] = sntl_ds['WTEQ']*2.54
sntl_ds['WTEQ']  = sntl_ds['WTEQ'].assign_attrs({'units':'cm'})

sntl_ds['PREC'] = sntl_ds['PREC']*2.54
sntl_ds['PREC']  = sntl_ds['PREC'].assign_attrs({'units':'cm'})


# outpath = '/storage/dlhogan/sos/data'
outpath = '/storage/dlhogan/sos/data'
if __name__ == "__main__":
    sntl_ds.to_netcdf(f"{outpath}{filename}_{edate.strftime(format='%Y%m%d')}.nc")
