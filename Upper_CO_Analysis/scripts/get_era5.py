''' This script is meant to grab ERA5 reanalysis monthly precipitation totals for water years 1964-2022 (October 1963-September 2022) for the Upper Colorado River Basin.
It will save the downloaded data as a netcdf file over a regular grid over the UCRB.
We will then filter the output to only include the UCRB and save it as a new netcdf file.
We will create another gridded average output for grid cells covering all HCDN basins in the analys.
NOTE: ERA5 is approximately 30 km resolution, so smaller basins will be represented with a single grid cell.
'''
import cdsapi
import os 
import geopandas as gpd
import rioxarray as rxr
import xarray as xr
import timeit


def download_era5(file_format, folder_raw, downloaded_file, start_year, end_year, variables_list, lat_min, lon_min, lat_max, lon_max):
    """
    This function downloads ERA5 data from the Copernicus Climate Data Store (CDS) using the cdsapi python package. 
    It will download the data to the specified folder and save it as a netcdf file.
    file_format: 'grib' or 'netcdf' (but ONLY netcdf is supported by the code below for mapping and time serie extraction)
    folder_raw: folder where to save the netcdf file
    downloaded_file: name of the netcdf file to be saved
    start_year: first year of the period to download
    end_year: last year of the period to download
    variables_list: list of variables to download
    lat_min, lon_min, lat_max, lon_max: coordinates of the area to download

    """
    # +++++++ Download
    years = [ str(start_year +i ) for i in range(end_year - start_year + 1)]                   
    if not os.path.exists(folder_raw): 
        os.mkdir(folder_raw)

    downloaded_file = os.path.join(folder_raw, downloaded_file)
    if not os.path.exists(os.path.join(folder_raw, downloaded_file)):
        print('Process started. Please wait the ending message ... ')
        start = timeit.default_timer()
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-land-monthly-means',
            {
                'format': file_format,                                  
                'product_type': 'monthly_averaged_reanalysis',
                'variable': variables_list,                   
                'year': years,
                'month': [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ],
                'time': '00:00',
                'area': [ lat_min, lon_min, lat_max, lon_max ],
            }, downloaded_file
            )

        stop = timeit.default_timer()
        print('Process completed in ', (stop - start)/60, ' minutes')
        return
    else: 
        print('File already downloaded')
        return

def set_units(ds, variable):
        # +++++++ Unit conversion
    # https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation
    param_mean = ['sd', 't2m']    # parameters to be averaged by time step (not summed)
    param_negative = ['pev', 'e', 'evaow', 'evabs']    # negative parameters to be transformed positive
    param_meter = ['tp', 'sro', 'ssro', 'ro', 'sd', 'pev', 'e', 'evaow', 'evabs']# Parameters in meter to be converted in mm
    param_temp = ['t2m']

    if variable=='total_precipitation':
        param = 'tp'
    elif variable=='surface_runoff':
        param = 'sro'
    elif variable=='sub_surface_runoff':
        param = 'ssro'
    elif variable=='runoff':
        param = 'ro'
    elif variable=='2m_temperature':
        param = 't2m'
    elif variable=='snow_depth_water_equivalent':# Implementation to be confirmed
        param = 'sd'
    elif variable=='potential_evaporation':
        param = 'pev'
    elif variable=='total_evaporation':
        param = 'e'
    elif variable=='evaporation_from_open_water_surfaces_excluding_oceans':
        param = 'evaow'
    elif variable=='evaporation_from_bare_soil':
        param = 'evabs'
    else:
        print("EXECUTION ABORTED because the script currently works only for total_precipitation, surface_runoff, sub_surface_runoff, runoff, 2m_temperature, snow_depth_water_equivalent, potential_evaporation, total_evaporation, evaporation_from_open_water_surfaces_excluding_ocean and evaporation_from_bare_soil")
        quit()

    # units = ds[param].attrs['units']
    if param in param_temp:
        ds[param] = ds[param]   - 273.15
    #    ds.assign_attrs(attrs)
    #    ds[param].attrs['units'] = '°C'
    #    ds[param].attrs['long_name'] = long_name
        units = '°C'
        
    if param in param_negative:
        ds[param]  = ds[param]  * -1.

    if param in param_mean and param in param_meter:
        # Converts m to mm (without time step correction) e.g. monthly averaged snow stock in m/day does not has to be summed over month nor over year
        ds[param]  = ds[param]  * 1000.
        units = 'mm'
    elif param in param_meter:
        # Converts m/day to mm/month (https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation)
        ds[param]  = ds[param] * 1000. * ds[param].time.dt.days_in_month
        units = 'mm'

    # ds[param].attrs.update(units=units)
    return ds

def clip_to_ucrb(old_path, new_path, variable_list, lat_min=35, lat_max=44, lon_min=-113, lon_max=-105):
    if not os.path.exists(new_path):
        print('Clipping to UCRB and saving to netcdf...')
        ucrb_boundary = gpd.read_file('../data/geodata/Upper_Colorado_River_Basin_Boundary.json')
        # read in the new netcdf file
        era5land_nc = xr.open_dataset(old_path)
        # Clip to the UCRB
        if lat_min!=None and lat_max!=None and lon_min!=None and lon_max!=None:
            #era5land_nc.rio.set_crs('epsg:4326')
            #era5land_nc = era5land_nc.rio.clip_box(lon_min, lat_min, lon_max, lat_max)
            mask_lon = (era5land_nc.longitude >= lon_min) & (era5land_nc.longitude <= lon_max)
            mask_lat = (era5land_nc.latitude >= lat_min) & (era5land_nc.latitude <= lat_max)
            era5land_nc = era5land_nc.where(mask_lon & mask_lat, drop=True)
        # adjust units
        for var in variables_list:
            era5land_nc = set_units(era5land_nc, var)
        era5land_nc.to_netcdf(new_path)
        # close the data
        era5land_nc.close()
        print('Done!')
        return
    else:
        print('File already clipped to UCRB and located at: ', new_path)
        return
        # +++++++ Area clipping

if __name__ == '__main__':
    # +++++++ Customization
    file_format = 'netcdf'  # 'grib' or 'netcdf' (but ONLY netcdf is supported by the code below for mapping and time serie extraction)
    folder_raw = '/storage/dlhogan/sos/data/ERA5'
    folder_processed = '/home/dlhogan/GitHub/Spring-Precipitation-Effect-CO-River/Upper_CO_Analysis/data/precipdata'
    downloaded_file = 'ERA5-land-monthly-1963-2022.nc'
    # ....... AREA to extract
    lon_min, lat_min, lon_max, lat_max =[-113, 35,-105, 44]# UCRB


    # ....... PERIOD to extract
    start_year = 1963                                            # from 1963 
    end_year = 2022                                             # to 2022

    # ....... VARIABLE(S) to extract: single name or list of names among those below
    #         - total_precipitation, surface_runoff,  runoff, snow_depth_water_equivalent (m)
    #         - 2m_temperature (K)
    #         - potential_evaporation, total_evaporation, evaporation_from_open_water_surfaces_excluding_ocean, evaporation_from_bare_soil (m negative)
    variables_list = ['total_precipitation',
                    'potential_evaporation', 
                    ]
    download_era5(file_format, folder_raw, downloaded_file, start_year, end_year, variables_list, lat_min, lon_min, lat_max, lon_max)
    clip_to_ucrb(os.path.join(folder_raw, downloaded_file), os.path.join(folder_processed, 'ERA5-land-monthly-1963-2022-UCRB.nc'), variables_list, lat_min, lat_max, lon_min, lon_max)


