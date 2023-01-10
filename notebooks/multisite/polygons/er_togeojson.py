import geopandas as gpd
import fiona 
fiona.drvsupport.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['KMZ'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
# This is the polygon of the East River below the Pumphouse down to Mt. Crested Butte 
east_river_polygon_at_BC = gpd.read_file("East_River.kml", driver='KML')
east_river_polygon_at_BC = east_river_polygon_at_BC.to_crs('32613')

east_river_polygon_at_BC.to_file('east_polygon.json')