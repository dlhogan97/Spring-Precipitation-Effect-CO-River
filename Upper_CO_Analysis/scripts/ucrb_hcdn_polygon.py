# %%
import geopandas as gpd
import xarray as xr
import pandas as pd

# from metloom.pointdata import SnotelPointData, USGSPointData, MesowestPointData
import datetime as dt
import matplotlib.pyplot as plt

# Get UCRB hcdn stations taken from the USGS 2011 dataset
ucrb_hcdn_stations = gpd.read_file('./ucrb_hcdn_co_gdf_final.json')

# Read in Upper CO dataset
basins = gpd.read_file(r"C:\Users\dlhogan\OneDrive - UW\Documents\GitHub\sublimation_of_snow\data\bas_nonref_WestMnts.shp")

# Add 0 to create station ids
ucrb_hcdn_stations['STAID'] = ['0'+str(id) for id in ucrb_hcdn_stations['STAID']]

ucrb_hcdn_co_gdf = ucrb_hcdn_stations.to_crs(basins.crs)
ucrb_hcdn_co_gdf = ucrb_hcdn_co_gdf.drop('index_right',axis=1)

ucrb_hcdn_combined = gpd.sjoin(basins,ucrb_hcdn_co_gdf)
# old version
# %%
# ucrb_hcdn_stations = gpd.read_file('./ucrb_hcdn_co_gdf_final.json')
# ucrb_hcdn_stations['STAID'] = ['0'+str(station) for station in ucrb_hcdn_stations['STAID']]

# # %%
# basins = gpd.read_file(r"C:\Users\dlhogan\OneDrive - UW\Documents\GitHub\sublimation_of_snow\data\bas_ref_all.shp")

# # %%
# basins = basins.to_crs(epsg='4326')

# # %%
# ucrb_hcdn_basins = basins[basins['GAGE_ID'].isin(ucrb_hcdn_stations['STAID'])].reset_index(drop=True)

# # %%
# ucrb_hcdn_basins.to_file('./ucrb_hcdn_polygons.json',driver='GeoJSON')

# %%



