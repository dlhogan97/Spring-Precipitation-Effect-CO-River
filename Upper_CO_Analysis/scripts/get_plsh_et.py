import numpy as np
import os
import xarray as xr
import geopandas as gpd
import rioxarray as rxr
import nctoolkit as nc
# this wont work right now, but will update later
years = np.arange(1982,2014)
ucrb_boundary_4326 = gpd.read_file('../data/geodata/Upper_Colorado_River_Basin_Boundary.json').to_crs(4326)
for year in years:
    if not os.path.exists(f'../data/etdata/P-LSH_ET/UCRB_Monthly_ET_{year}.nc'):
        # download the data
        print('Downloading data...')
        url = f'http://files.ntsg.umt.edu/data/ET_global_monthly/Global_8kmResolution/Global_Monthly_ET_{year}.nc'
        print('Clipping to UCRB...')
        p_lsh_et = nc.open_url(url).to_xarray()
        # clip to UCRB
        p_lsh_et = p_lsh_et.where((p_lsh_et.LAT>35) &
                    (p_lsh_et.LAT<45) &
                    (p_lsh_et.LON>-115) &
                    (p_lsh_et.LON<-100) &
                    (p_lsh_et.monthly_ET>0),drop=True)
        monthly_ds_list = []
        # isolate each timestep
        for i in p_lsh_et.time:
            # isolate each timestep
            p_lsh_et_i = p_lsh_et.sel(time=i)
            # convert to a dataframe
            df = p_lsh_et_i.to_dataframe()
            # make pivot table
            df = df.pivot_table(values='monthly_ET',index='LAT',columns='LON')
            # convert to xarray with lat and lon dimensions
            ds = xr.DataArray(df.values,dims=['LAT','LON',],coords={'LAT':df.index,'LON':df.columns})
            ds = ds.rio.write_crs(4326)
            df = ds.rio.set_spatial_dims('LON','LAT')
            ds = ds.rio.clip(ucrb_boundary_4326.geometry)
            # add time as a coordinate
            ds = ds.assign_coords(time=i)
            monthly_ds_list.append(ds)
        print('Concatentating data...')
        # combine all the dataarrays into a single dataset
        monthly_ds = xr.concat(monthly_ds_list,dim='time')
        # rename the variable
        monthly_ds.name = 'monthly_ET'
        # add a units attribute to the variable
        monthly_ds.attrs['units'] = 'mm'
        print('Saving data...')
        # save to netcdf
        monthly_ds.to_netcdf(f'../data/etdata/P-LSH_ET/UCRB_Monthly_ET_{year}.nc')

        # delete the original file
        nc.deep_clean()
        print('Deleted original file.')
    else:
        print('File already exists.')