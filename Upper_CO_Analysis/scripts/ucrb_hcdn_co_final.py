import pandas as pd
import geopandas as gpd 

hcdn_stations = pd.read_excel('../../data/gagesII_sept30_2011_conterm.xlsx')
hcdn_stations_gdf = gpd.GeoDataFrame(hcdn_stations, geometry=gpd.points_from_xy(hcdn_stations.LNG_GAGE, hcdn_stations.LAT_GAGE))

hcdn_stations_gdf_filtered = hcdn_stations_gdf[
    (hcdn_stations_gdf['STATE'].isin(['CO'])) &
    ((hcdn_stations_gdf['HCDN-2009']=='yes') |
    (hcdn_stations_gdf['OLD_HCDN']=='yes'))
]

hcdn_stations_gdf_filtered = hcdn_stations_gdf_filtered.set_crs(epsg=4326)

ucrb_basin_boundary = gpd.read_file('../multisite/polygons/Upper_Colorado_River_Basin_Boundary.json')
ucrb_hcdn_co = gpd.sjoin(ucrb_basin_boundary, hcdn_stations_gdf_filtered)

ucrb_hcdn_co_gdf = gpd.GeoDataFrame(ucrb_hcdn_co, geometry=gpd.points_from_xy(ucrb_hcdn_co.LNG_GAGE, ucrb_hcdn_co.LAT_GAGE))
ucrb_hcdn_co_gdf.to_file('./ucrb_hcdn_co_gdf_final.json', driver='GeoJSON')