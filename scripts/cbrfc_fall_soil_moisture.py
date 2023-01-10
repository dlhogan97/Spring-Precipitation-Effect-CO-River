

"""
This script will grab available gridded fall soil moisture output from the operational model from CBRFC and save it as a netcdf to location
Author: Daniel Hogan
Date: Jan 9, 2023
"""

# Package imports
import numpy as np
import xarray as xr
import gzip

# Create grid for data
xllcorner=-116.00416667027
yllcorner=29.99583333096
cellsize=0.00833333333
nrows=1321
ncols=1681
lat = []
lon = []
for i in range(nrows):
    if i == 0:
        lon.append(xllcorner)
    else:
        lon.append(lon[i-1]+cellsize)
for i in range(ncols):
    if i == 0:
        lat.append(yllcorner)
    else:
        lat.append(lat[i-1]+cellsize)
lat=lat[::-1]

# Set years where we have data (missing 2015 and 2016)
years = np.arange(1980,2023,1)
    # available urls
url_list =[
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111980.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111981.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111982.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111983.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111984.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111985.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111986.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111987.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111988.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111989.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111990.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111991.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111992.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111993.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111994.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111995.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111996.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111997.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111998.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15111999.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112000.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112001.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112002.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112003.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112004.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112005.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112006.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112007.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112008.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112009.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112010.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112011.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112012.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112013.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/histsoilpct/histsoilpct.trima.15112014.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112015.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112016.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.16112017.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112018.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112019.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112020.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.15112021.gz',
    'https://www.cbrfc.noaa.gov/rmap/grid800/asc/soilfall/soilfall.trima.02112022.gz',
]

def cbrfc_soil_moisture(urls, years, outpath):
    # Set dimensions to years lat and lon
    dims = ('year','lat', 'lon')
    
    # create an empty dataset filled with variables that I want
    combined_ds = xr.Dataset(
            data_vars={'soil_moisture': (dims, np.zeros((len(years),len(lat),len(lon))))},
            coords={'year': years, 'lat':lat, 'lon':lon})
    
    # Iterate over each year and grab the data that I want
    for i,year in enumerate(years):
        print(year)
        if year in [2015, 2016]:
            print(f'Data not availble for {year}')
            continue
        else:
            # Grab the data from the urls provided
            cbrfc_data = pd.read_csv(urls[i], compression='gzip',delim_whitespace=True,skiprows=6, header=None)
            ds = xr.DataArray((100*cbrfc_data).to_numpy(),dims={'lat':lat,'lon':lon})
        combined_ds.loc[dict(year=year)] = ds
    combined_ds = combined_ds.where(combined_ds>0, np.nan)
    combined_ds.to_netcdf(outpath)
    return combined_ds

if __name__ == 'main':
    outpath = '../../../../../../storage/dlhogan/sos/data/cbrfc_fall_soil_product.nc'
    cbrfc_ds = cbrfc_soil_moisture(url_list,years, outpath)