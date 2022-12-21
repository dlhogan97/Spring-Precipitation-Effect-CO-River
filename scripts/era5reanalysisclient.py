"""Created by Danny Hogan 12/19/2022
Installs relevant volumetric soil moisture data and relavent surface meteorology information from ERA5 from a defined area for the years, months and days specified
this includes 2m temperature, evaporation, potential evaporation, soil moisutre and temperature at different levels 0.07 (0–0.07), 0.21 (0.07–0.28), 0.72 (0.28–1.00) and 1.89 (1.00–2.89) m.
Thus the first three levels are the most relevant to distributed measurements.
"""
import cdsapi
import os 

years = input("Years to pull (years, separated by comma):")

years = years.split(sep=',')
years = [year.removeprefix(' ') for year in years ]

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'grib',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            '2m_temperature', 'evaporation', 'potential_evaporation',
            'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
            'soil_temperature_level_4', 'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
            'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
        ],
        'year': years,
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'time': '00:00',
        'area': [
            40, -108, 36,
            -104,
        ],
    },
    f'../../../../../../storage/dlhogan/sos/data/ERA5/{years[0]}_to_{years[-1]}.grib')