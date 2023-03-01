import glob
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

from metloom.pointdata import SnotelPointData
from dataretrieval import nwis

import datetime as dt

import geopandas as gpd
import contextily as cx


# Polygon for the East and Taylor Rivers
east_taylor_polygon = gpd.read_file('../multisite/polygons/east_taylor.json')

# Pull in SNTL data and Locations

snotel_point = SnotelPointData("380:CO:SNTL", "Butte")
butte_loc = snotel_point.get_daily_data(
    dt.datetime(2020, 1, 2), dt.datetime(2020, 1, 2),
    [snotel_point.ALLOWED_VARIABLES.SWE]
).geometry.iloc[0]

snotel_point = SnotelPointData("680:CO:SNTL", "Park Cone")
park_cone_loc = snotel_point.get_daily_data(
    dt.datetime(2020, 1, 2), dt.datetime(2020, 1, 2),
    [snotel_point.ALLOWED_VARIABLES.SWE]
).geometry.iloc[0]

snotel_point = SnotelPointData("737:CO:SNTL", "Schofield Pass")
schofield_pass_loc = snotel_point.get_daily_data(
    dt.datetime(2020, 1, 2), dt.datetime(2020, 1, 2),
    [snotel_point.ALLOWED_VARIABLES.SWE]
).geometry.iloc[0]

snotel_point = SnotelPointData("1141:CO:SNTL", "Upper Taylor")
upper_taylor_loc = snotel_point.get_daily_data(
    dt.datetime(2020, 1, 2), dt.datetime(2020, 1, 2),
    [snotel_point.ALLOWED_VARIABLES.SWE]
).geometry.iloc[0]

# Get locations of streamgage sites
site_info = nwis.get_info(sites=['09112500','09107000 '])
site_info_pts = gpd.GeoDataFrame(site_info[0], geometry=gpd.points_from_xy(site_info[0]['dec_long_va'],site_info[0]['dec_lat_va']))
site_info_pts = site_info_pts.set_crs('4326')
gage_pts_local = site_info_pts.to_crs(east_taylor_polygon.crs)

# Build basemap
sntl_gdf = gpd.GeoSeries([butte_loc,park_cone_loc,schofield_pass_loc,upper_taylor_loc]).set_crs('4326')
sntl_gdf_local = sntl_gdf.to_crs(east_taylor_polygon.crs)

UCR_basin = gpd.read_file('../multisite/polygons/Upper_Colorado_River_Basin_Boundary.json')
east_taylor_polygon_4326 = east_taylor_polygon.to_crs(epsg='4326')

fig, axs = plt.subplots(ncols=2, figsize=(18,18))

# First plot for UCR basin
ax=axs[0]
# Plot basin and boundary
UCR_basin.plot(ax=ax, alpha=0.25)
# UCR_basin.boundary.plot(ax=ax, color='k')

# Add text for UC River Basin
ax.text(UCR_basin.centroid.x.values[0], 
        UCR_basin.centroid.y.values[0], 
        'Upper Colorado\nRiver Basin',
        fontsize=20, 
        fontweight='bold',
        horizontalalignment='center')

# Add east/taylor river basin centroid and text
ax.scatter(east_taylor_polygon_4326.centroid[0].x, 
        east_taylor_polygon_4326.centroid[0].y, 
        s=100, 
        label='East/Taylor Basins', color='red', ec='k')
ax.text(east_taylor_polygon_4326.centroid.x.values[0], 
        east_taylor_polygon_4326.centroid.y.values[0]-0.7, 
        'East/Taylor\nRiver Basins',
        fontsize=12, 
        fontweight='bold',
        color='red',
        horizontalalignment='center')

# Add basemap
cx.add_basemap(ax, crs=UCR_basin.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik)
# Create
ax.set_xlim(-114,-104)
ax.set_ylim(34.5,44)
ax.set_xlabel('Longitude', size=16)
ax.set_ylabel('Latitude', size=16)
ax.set_title('(a)', size=20)
# Switch to Localized Plot
ax=axs[1]
#Now making a basemap in contextily
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
east_taylor_polygon[east_taylor_polygon['name']=='Taylor River'].geometry.plot(color=CB_color_cycle[0], linewidth=3,edgecolor='k',alpha=0.25, ax=ax)
east_taylor_polygon[east_taylor_polygon['name']=='East River'].geometry.plot(color=CB_color_cycle[3], linewidth=3,edgecolor='k', alpha=0.25, ax=ax)

#Add north arrow, https://stackoverflow.com/a/58110049/604456
x1, y1, arrow_length = 0.9, 0.85, 0.07
ax.annotate('N', xy=(x1, y1), xytext=(x1, y1-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20,
            xycoords=ax.transAxes)
# Add scale-bar
x, y, scale_len = 379000, 4.3125e6, 5000 #arrowstyle='-'
scale_rect = patches.Rectangle((x,y),scale_len,200,linewidth=1,edgecolor='k',facecolor='k')
ax.add_patch(scale_rect)
ax.text(x+scale_len/2, y-1600, s='5 KM', fontsize=15, horizontalalignment='center')

# Add text for East River
ax.text(east_taylor_polygon[east_taylor_polygon['name']=='East River'].centroid.x.values[0], 
        east_taylor_polygon[east_taylor_polygon['name']=='East River'].centroid.y.values[0], 
        'East River',
        fontsize=20, 
        fontweight='bold',
        horizontalalignment='center')

# Add text for Taylor River
ax.text(east_taylor_polygon[east_taylor_polygon['name']=='Taylor River'].centroid.x.values[0], 
        east_taylor_polygon[east_taylor_polygon['name']=='Taylor River'].centroid.y.values[0], 
        'Taylor River',
        fontsize=20,
        fontweight='bold', 
        horizontalalignment='center')


#Add in SNOTELs as points
sntl_gdf_local.plot(c=CB_color_cycle[2], alpha=1, ec='k', label='SNOTEL Site', ax=ax, markersize=200)
#Add in SNOTELs as points
gage_pts_local.plot(c=CB_color_cycle[4], alpha=1, ec='k', label='USGS Streamgage', ax=ax, markersize=200)

#Now making a nice legend
ax.legend(loc='upper right', prop={'size': 16})
ax.set_xlabel('Easting (m)', size=16)
ax.set_ylabel('Northing (m)', size=16)
ax.set_title('(b)', size=20)
#Now adding in the basemap imagery
cx.add_basemap(ax, crs=east_taylor_polygon.crs.to_string(), source=cx.providers.OpenTopoMap)
fig.savefig('./figures/east_taylor_overview.png')