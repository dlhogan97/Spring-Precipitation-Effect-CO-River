import pandas as pd

fn = r"C:\Users\dlhogan\Downloads\KP11-21-Jan.xml"

tmp_profile = pd.read_xml(fn)['temp_profile'][9]
depths_T = [float(j[0])/10 for j in [i.split(":") for i in tmp_profile.split(';')]]
temps = [float(j[1]) for j in [i.split(":") for i in tmp_profile.split(';')]]
temp_df = pd.Series(temps, index=depths_T)

density_profile = pd.read_xml(fn)['profile'][8]
depths_rho = [float(j[0])/10 for j in [i.split(":") for i in density_profile.split(';')]]
density = [float(j[1]) for j in [i.split(":") for i in density_profile.split(';')]]
density_df = pd.Series(density, index=depths_rho)