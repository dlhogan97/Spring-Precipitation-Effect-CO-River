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
site_ids = ["380:CO:SNTL", "680:CO:SNTL", "737:CO:SNTL"]
API_DOMAIN = "https://api.snowdata.info/"

# grabs input
edate = input('Type start date (format %Y%m%d): ')
edate = datetime.strptime(edate,'%Y%m%d')

def get_awdb_data(
    site_ids,
    elements=["SMS","TAVG","WTEQ","PREC"],
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

sntl_dfs = get_awdb_data(site_ids=site_ids)

for i,df in enumerate(sntl_dfs):
    df.index = pd.to_datetime(df.index)
    sntl_dfs[i] = df

# adding datetime as needed and filtering to 2015
sntl_df_dict = {
    'Butte_'+site_ids[0]:pd.concat(sntl_dfs[0:4], axis=1).sort_index().to_xarray(),
    'ParkCone_'+site_ids[1]:pd.concat(sntl_dfs[4:8], axis=1).sort_index().to_xarray(),
    'SchofieldPass_'+site_ids[2]:pd.concat(sntl_dfs[8:], axis=1).sort_index().to_xarray(),
}
sntl_ds = xr.concat(sntl_df_dict.values(), pd.Index(sntl_df_dict.keys(), name='Location'))
sntl_ds = sntl_ds.assign_coords({'WY':sntl_ds.Date.dt.year.where(sntl_ds.Date.dt.month < 10, sntl_ds.Date.dt.year + 1)})

if __name__ == "__main__":
    if not os.path.exists(f"../../../../../../storage/dlhogan/sos/data/east_river_sntl_{edate.strftime(format='%Y%m%d')}.nc"):
        sntl_ds.to_netcdf(f"../../../../../../storage/dlhogan/sos/data/east_river_sntl_{edate.strftime(format='%Y%m%d')}.nc")
