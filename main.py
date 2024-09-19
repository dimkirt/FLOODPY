# Convert Notebook to script

import time
import datetime

# --- Cell 1
# The path of your project. Make sure you have enough free space disk on the specific location.
projectfolder = '~/projects/floods'

# The location of floodpy code 
src_dir = '~/FLOODPY/floodpy'

# SNAP ORBIT DIRECTORY
snap_orbit_dir = '~/.snap/auxdata/Orbits/Sentinel-1' # Mac OS

# SNAP GPT full path
GPTBIN_PATH = '/Applications/esa-snap/bin/gpt' # Mac OS

# The start and end datetimes for Pre-flood time span and flood time span (Format is YYYYMMDDTHHMMSS in UTC)
pre_flood_start = '20230701T030000'
pre_flood_end = '20230903T030000'
flood_start = '20230903T030000'
flood_end = '20230909T030000'

# Flood event spatial information 
# - You can provide AOI VECTOR FILE or AOI BBOX. 
# - Please ensure that your AOI BBOX has dimensions smaller than 100km x 100km
# - If you provide AOI VECTOR, AOI BBOX parameters will be ommited
# - In case you provide AOI BBOX coordinates, set  AOI_File = None

# AOI VECTOR FILE (if given AOI BBOX parameters can be ommited)
AOI_File = "None"

# AOI BBOX (WGS84)
LONMIN = 21.82
LATMIN = 39.35
LONMAX = 22.30
LATMAX = 39.65

# Data access and processing
# The number of Sentinel-1 relative orbit. The default 
#       value is Auto. Auto means that the relative orbit that has
#       the Sentinel-1 image closer to the Flood_datetime is selected. 
#       S1_type can be GRD or SLC.
relOrbit = 'Auto' 

# The minimum mapping unit area in square meters
minimum_mapping_unit_area_m2=4000

# Computing resources to employ
CPU=7
RAM='31'


# Credentials for Sentinel-1/2 downloading
Copernicus_username = ""
Copernicus_password = ""

# --- Cell 2

params_dict = {'projectfolder':projectfolder,
            'src_dir' : src_dir,
            'snap_orbit_dir' : snap_orbit_dir,
            'GPTBIN_PATH' : GPTBIN_PATH,
            'pre_flood_start' : pre_flood_start,
            'pre_flood_end' : pre_flood_end,
            'flood_start' : flood_start,
            'flood_end' : flood_end,
            'AOI_File' : AOI_File,
            'LONMIN' : LONMIN,
            'LATMIN' : LATMIN,
            'LONMAX' : LONMAX,
            'LATMAX' : LATMAX,
            'relOrbit' : relOrbit,
            'minimum_mapping_unit_area_m2' : minimum_mapping_unit_area_m2,
            'CPU' : CPU,
            'RAM' : RAM,
            'Copernicus_username' : Copernicus_username,
            'Copernicus_password' : Copernicus_password,
            }

# --- Cell 3
import os
import numpy as np
import rasterio as rio
import rasterio.mask
import geopandas as gpd
import pandas as pd
import xarray as xr

# plotting functionalities
import matplotlib.pyplot as plt
import folium
import matplotlib
from branca.element import Template, MacroElement
import branca.colormap as cm
from folium.plugins import MeasureControl, Draw
from xyzservices.lib import TileProvider

# FLOODPY libraries
from floodpy.utils.folium_categorical_legend import get_folium_categorical_template
from floodpy.FLOODPYapp import FloodwaterEstimation

# --- Cell 4
Floodpy_app = FloodwaterEstimation(params_dict = params_dict)

# --- Cell 5 -- needs sudo to access the project dir
Floodpy_app.download_landcover_data()

# --- Cell 6
Floodpy_app.download_ERA5_Precipitation_data()

# --- Cell 7 -- Doesnt work on the local script figure doesnt show
Floodpy_app.plot_ERA5_precipitation_data()

# --- Cell 8
Floodpy_app.query_S1_data()
print('The available dates for flood mapping are: \n --> {}'.format('\n --> '.join(map(str, Floodpy_app.flood_candidate_dates))))

# --- Cell 9
sel_flood_date = '2023-09-06T04:39:47.095652000' # This number needs to be taken from one of the printed results of the previus cell

# --- Cell 10
Floodpy_app.sel_S1_data(sel_flood_date)

# --- Cell 11
Floodpy_app.download_S1_GRD_products()

# --- Cell 12
Floodpy_app.download_S1_orbits()

# --- Cell 13 - takes some time, it does all the preprocessing or it hangs?
now = datetime.datetime.now()
print("\nStart create_S1_stack, time now: {}".format(now))
start_time = time.time()

Floodpy_app.create_S1_stack(overwrite=False)

end_time = time.time()
now = datetime.datetime.now()
print("\nEnd create_S1_stack, time now: {}".format(now))
print(f"Execution time: {end_time - start_time:.4f} seconds")

# --- Cell 14
S1_stack = xr.open_dataset(Floodpy_app.S1_stack_filename)
S1_stack['VV_dB'].drop_duplicates(dim=...).plot(x="x", y="y", col="time", col_wrap=3, vmin=-22, vmax=5)