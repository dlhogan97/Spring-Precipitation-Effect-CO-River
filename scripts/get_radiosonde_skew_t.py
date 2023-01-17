import act
from soslib import funcs
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd

import metpy.calc as mpcalc
from metpy.plots import Hodograph, SkewT
from metpy.units import units

date_start = input("One day of sondes.\nDate and Time for Radiosonde Start (format YY-MM-DDTHH:MM:SS): ")
date_end = input("Date and Time for Radiosonde End (format YYYY-MM-DD): ")
one_or_two = input("Y/N for two plots to be produced: ")
# Personal access necessary for downloading from the ARM portal, need an account to due so
username = 'dlhogan@uw.edu'
token = '7f1c805e6ae94c21'
radiosonde ='gucsondewnpnM1.b1'

start = date_start[0:10]
end = date_end[0:10]

def plot_skewT(ds):
    # Create a new figure. The dimensions here give a good aspect ratio
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=30)

    p = ds.pres.values * units.hPa
    t = ds.tdry.values * units.degC
    td = mpcalc.dewpoint_from_relative_humidity(ds.tdry,ds.rh)
    u = ds.u_wind
    v = ds.v_wind

    # Calculate the LCL
    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], t[0], td[0])

    # Calculate the parcel profile.
    parcel_prof = mpcalc.parcel_profile(p, t[0], td[0]).to("degC")

    # Set spacing interval--Every 50 mb from pmax to 100 mb
    plot_interval = np.arange(100, max(p.magnitude), 50) * units('hPa')
    # Get indexes of values closest to defined interval
    ix = mpcalc.resample_nn_1d(p, plot_interval)

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, t, 'r')
    skew.plot(p, td, 'g')
    skew.plot_barbs(p[ix], u[ix], v[ix])
    skew.ax.set_ylim(max(p), 100)
    skew.ax.set_xlim(min(t.magnitude)-10, max(t.magnitude)+20)

    # Plot LCL as black dot
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # Plot the parcel profile as a black line
    skew.plot(p, parcel_prof, 'k', linewidth=2)

    # Shade areas of CAPE and CIN
    skew.shade_cin(p, t, parcel_prof, td)
    skew.shade_cape(p, t, parcel_prof)

    # Plot a zero degree isotherm
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()

    # Create a hodograph
    # Create an inset axes object that is 40% width and height of the
    # figure and put it in the upper right hand corner.
    ax_hod = inset_axes(skew.ax, '40%', '40%', loc=1)
    h = Hodograph(ax_hod, component_range=20.,)
    h.add_grid(increment=20)
    h.plot_colormapped(u[ix], v[ix], ds.wspd[ix])  # Plot a line colored by wind speed

    start_hour = ds.time.dt.hour[0]
    # Save the plot
    plt.savefig(f'../figures/radiosondes/SAIL_sonde_{start}_{start_hour}UTC.png')
    # Show the plot
    plt.show()
    return

# Download SAIL sonde data
try:
    sonde1_start = dt.datetime.strptime(date_start,'%Y-%m-%dT%H:%M:%S')
    sonde1_end = sonde1_start + dt.timedelta(hours=6)

    sonde_ds = funcs.get_sail_data(username, token, radiosonde, start, end)

    sonde1 = sonde_ds.sel(time=slice(sonde1_start,sonde1_end))
    if one_or_two == 'Y':
        sonde2_start = sonde1_end + dt.timedelta(hours=6)
        sonde2_end = sonde2_start + dt.timedelta(hours=6)
    
        sonde2 = sonde_ds.sel(time=slice(sonde2_start,sonde2_end))
    plot_skewT(sonde1)
    if one_or_two == "Y":
        plot_skewT(sonde2)
except: 
    print('Data not found, may not be loaded yet.')


