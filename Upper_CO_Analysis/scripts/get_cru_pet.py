import numpy as np
import os
import xarray as xr
import geopandas as gpd
import rioxarray as rxr
import urllib.request
import gzip

if not os.path.exists('../data/etdata/CRU_UCRB_Monthly_PET_1963_2022.nc'):
    url = 'https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/pet/cru_ts4.07.1901.2022.pet.dat.nc.gz'
    filepath = '../data/etdata/'+url.split('/')[-1]
        
    filehandle, _ = urllib.request.urlretrieve(url, filepath)
    # write to file using gzip
    with gzip.open(filepath, 'rb') as f_in:
        with open('../data/etdata/CRU_UCRB_Monthly_PET_1901_2022.nc', 'wb') as f_out:
            f_out.write(f_in.read())
    # open the file
    pet = xr.open_dataset('../data/etdata/CRU_UCRB_Monthly_PET_1901_2022.nc')
    ucrb_boundary_4326 = gpd.read_file('../data/geodata/Upper_Colorado_River_Basin_Boundary.json').to_crs(4326)
    # rename lat to y and lon to x
    pet = pet.rename({'lat':'y','lon':'x'})
    pet = pet.rio.write_crs(4326)
    # clip to UCRB
    pet = pet.rio.clip(ucrb_boundary_4326.geometry)
    # clip the time dimension to begin in 1963
    pet = pet.where(pet.time.dt.year>1962,drop=True)
    # multiply each pet value by the days in each month
    pet = pet * pet.time.dt.days_in_month

    # save to netcdf
    pet.to_netcdf('../data/etdata/CRU_UCRB_Monthly_PET_1963_2022.nc')
    print('Data saved.')
    # remove the original file
    os.remove('../data/etdata/cru_ts4.07.1901.2022.pet.dat.nc.gz')
    os.remove('../data/etdata/CRU_UCRB_Monthly_PET_1901_2022.nc')
    print('Deleted original files.')
else:
    print('File already exists.')

if not os.path.exists('../data/etdata/CRU_UCRB_MONTHLY_TCC_1963_2022.nc'):
    # url = 'https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/cld/cru_ts4.07.1901.2022.cld.dat.nc.gz'
    # filepath = '../data/etdata/'+url.split('/')[-1]
        
    # filehandle, _ = urllib.request.urlretrieve(url, filepath)
    # # write to file using gzip
    # with gzip.open(filepath, 'rb') as f_in:
    #     with open('../data/etdata/CRU_UCRB_Monthly_TCC_1901_2022.nc', 'wb') as f_out:
    #         f_out.write(f_in.read())
    # open the file
    tcc = xr.open_dataset('../data/etdata/CRU_UCRB_Monthly_TCC_1901_2022.nc')
    ucrb_boundary_4326 = gpd.read_file('../data/geodata/Upper_Colorado_River_Basin_Boundary.json').to_crs(4326)
    # rename lat to y and lon to x
    tcc = tcc.rename({'lat':'y','lon':'x'})
    tcc = tcc.rio.write_crs(4326)
    # clip to UCRB
    tcc = tcc.rio.clip(ucrb_boundary_4326.geometry)
    # clip the time dimension to begin in 1963
    tcc = tcc.where(tcc.time.dt.year>1962,drop=True)

    # save to netcdf
    tcc.to_netcdf('../data/etdata/CRU_UCRB_Monthly_tcc_1963_2022.nc')
    print('Data saved.')
    # remove the original file
    os.remove('../data/etdata/cru_ts4.07.1901.2022.cld.dat.nc.gz')
    os.remove('../data/etdata/CRU_UCRB_Monthly_tcc_1901_2022.nc')
    print('Deleted original files.')
else:
    print('File already exists.')    