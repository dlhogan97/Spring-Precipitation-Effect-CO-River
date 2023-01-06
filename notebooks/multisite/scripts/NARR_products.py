import xarray as xr
import numpy as np
import geopandas as gpd
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

def get_narr_precip(year, centroid):
    """Grabs the precipitation product from NARR surrounding the 6 grid cells around a given centroid

    Args:
        year (int): Year to grab data from
        centroid (tuple): Tuple or list containing the centroid of the center point.

    Returns:
        ds, annual_precip: returns the dataset containing daily data and the annual total precipitation for the given area in kg/m2 or mm
    """
    urlpath_prev =f"https://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/Dailies/monolevel/apcp.{year-1}.nc"
    urlpath_current =f"https://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/Dailies/monolevel/apcp.{year}.nc"
    ds_previous = xr.open_dataset(urlpath_prev,decode_coords="all")
    ds_current = xr.open_dataset(urlpath_current,decode_coords="all")

    ds = xr.concat([trim_ds(ds_previous,(38,-107)),trim_ds(ds_current,(38,-107))],dim='time')
    ds_wy = ds.sel(time=slice(f'{year-1}-10-1',f'{year}-9-30'))
    
    annual_precip = (ds_wy.apcp.sum()/(ds_wy.apcp.shape[1]*ds_wy.apcp.shape[2])) # kg/m2 * km2 / 1000**2 m2/km2 / 1 m3/1000 kg
    return ds_wy, annual_precip.values

def trim_ds(ds, centroid):
    loc_lat = centroid[0]
    loc_lon = centroid[1]

    lat = ds.lat.values
    lon = ds.lon.values

    abs_lon = np.abs(lon - loc_lon)
    abs_lat = np.abs(lat - loc_lat)

    maxi = np.maximum(abs_lon,abs_lat)
    loc_index = np.argmin(maxi)


    ij = np.unravel_index(loc_index,(ds.dims['y'],ds.dims['x']))
    i_loc_index=ij[0]
    j_loc_index=ij[1]

    ds_local = ds.isel(y=slice(i_loc_index-1,i_loc_index+2),x=slice(j_loc_index-1,j_loc_index+1)).drop_dims('nbnds')
    return ds_local


gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
east_river_polygon = gpd.read_file("./East_River.kml", driver='KML')
centroid = east_river_polygon.centroid

# get all NARR precip data from the available years and store these values
years = np.arange(1980,2022,1)
narr_precip_totals = []
for year in years:
    if year % 10 == 0:
        print(f'Working in the {year}s')
    ds,annual_precip = get_narr_precip(year,(centroid.y.values, centroid.x.values))
    narr_precip_totals.append(annual_precip)

precip_df = pd.Series(narr_precip_totals,index=years, name='narr_precip_totals_mm')
precip_df.to_csv('./data/narr_precip_1980_2022.csv')