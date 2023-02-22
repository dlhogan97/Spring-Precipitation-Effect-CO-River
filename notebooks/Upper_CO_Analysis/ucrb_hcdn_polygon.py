# %%
import geopandas as gpd
import xarray as xr
import pandas as pd

# from metloom.pointdata import SnotelPointData, USGSPointData, MesowestPointData
import datetime as dt
import matplotlib.pyplot as plt

# %%
ucrb_hcdn_stations = gpd.read_file('./ucrb_hcdn_stations.json')
ucrb_hcdn_stations['station_id_str'] = ['0'+str(station) for station in ucrb_hcdn_stations['station_id']]

# %%
basins = gpd.read_file(r"C:\Users\dlhogan\OneDrive - UW\Documents\GitHub\sublimation_of_snow\data\bas_ref_all.shp")

# %%
basins = basins.to_crs(epsg='4326')

# %%
ucrb_hcdn_basins = basins[basins['GAGE_ID'].isin(ucrb_hcdn_stations['station_id_str'])].reset_index(drop=True)

# %%
ucrb_hcdn_basins.to_file('./ucrb_hcdn_polygons.json',driver='GeoJSON')

# %%



