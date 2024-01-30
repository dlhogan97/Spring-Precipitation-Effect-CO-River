"""
Use this script to download nClimGrid monthly precipitation data for the contiguous US. 
We will then filter the output to only include the UCRB and save it as a new netcdf file.
"""
# download nClimGrid using request from this s3 bucket: https://noaa-nclimgrid-monthly-pds.s3.amazonaws.com/nclimgrid_prcp.nc 
from urllib.request import urlretrieve
import os
import pandas as pd
import geopandas as gpd
import rioxarray as rxr
from cdo import * 
cdo = Cdo()
tmp_storage_path = '/storage/dlhogan/sos/data/nClimGrid/tmp'
final_storage_path = '/storage/dlhogan/sos/data/nClimGrid'
filename = 'nclimgrid_prcp.nc'
# check if the readme exists in tmp
if not os.path.exists(os.path.join(tmp_storage_path, 'readme.txt')):
    print('File does not exist. Downloading now...')
    url = 'https://noaa-nclimgrid-monthly-pds.s3.amazonaws.com/nclimgrid_prcp.nc'
    urlretrieve(url, os.path.join(tmp_storage_path, filename))
    
    # use cdo to trim the data to the UCRB
    cdo.sellonlatbox('-113,-105,35,44', input=os.path.join(tmp_storage_path,filename),output=os.path.join(final_storage_path,'ucrb_'+filename))
    # delete the raw data
    os.remove(os.path.join(tmp_storage_path, filename))
    # create an readme file and fill with information about where the data was downloaded from
    with open(os.path.join(tmp_storage_path, 'readme.txt'), 'w') as f:
        f.write('Data downloaded from https://noaa-nclimgrid-monthly-pds.s3.amazonaws.com/nclimgrid_prcp.nc.\n Data was filtered to UCRB and raw data was deleted')
        # close the file
        f.close()
else:
    print('File already exists, data was trimmed to UCRB and raw data was deleted to free up space.')
    # save the data to the precip folder
    new_storage_path = '../data/precipdata/nclimgrid_5km_ucrb.nc'
    if not os.path.exists(new_storage_path):
        print('Clipping to UCRB and saving to netcdf...')
        ucrb_boundary = gpd.read_file('../data/geodata/Upper_Colorado_River_Basin_Boundary.json')
        # read in the data
        nclimgrid = rxr.open_rasterio(os.path.join(final_storage_path,'ucrb_'+filename))
        # write crs to 4326
        nclimgrid.rio.write_crs(4326, inplace=True)
        # filter to the UCRB
        # clip nclimgrid to ucrb boundary
        nclimgrid = nclimgrid.rio.clip(ucrb_boundary.geometry, crs=4326)
        
        nclimgrid.to_netcdf(new_storage_path)
        # close the data
        nclimgrid.close()






