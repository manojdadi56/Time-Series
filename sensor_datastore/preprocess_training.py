#
# Imports
#

import pandas as pd
import numpy as np

import warnings
import itertools
warnings.filterwarnings("ignore")
import statsmodels.api as sm
import requests
import pandas as pd
import datetime
import pytz
from skimage import io
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
import os

from data_processing import dataProcessing
from azureml.core import Workspace

# Read data
sensor = pd.read_csv("./plot2-IoT Sensor Data.csv")
source_one = pd.read_csv("./plot2-Source 1 Weather.csv")
source_two =  pd.read_csv("./plot2-Source 2 Weather.csv")

processing = dataProcessing()


# Fill missing values
source_one_tc = processing.fill_missing_values(source_one, "TC")
source_two_tc = processing.fill_missing_values(source_two, "TC")
sensor_tc = processing.fill_missing_values(sensor, "TC")

source_one_hum = processing.fill_missing_values(source_one, "HUM")
source_two_hum = processing.fill_missing_values(source_two, "HUM")
sensor_hum = processing.fill_missing_values(sensor, "HUM")[:8760]

source_one_pre = processing.fill_missing_values(source_one, "PRES")
source_two_pre = processing.fill_missing_values(source_two, "PRES")
sensor_pre = processing.fill_missing_values(sensor, "PRES")[:8760]



#
# Merge all
#

sensor_tc.rename(columns = {'value':'target'}, inplace = True) 
source_one_tc.rename(columns = {'value':'value_one'}, inplace = True) 
source_two_tc.rename(columns = {'value':'value_two'}, inplace = True) 


temp_merge = pd.merge(sensor_tc, source_one_tc, on='datetime')
sensor_all = pd.merge(temp_merge, source_two_tc, on='datetime')
sensor_all['month'] = pd.DatetimeIndex(sensor_all['datetime']).month

"Any missing values : " +  str(sensor_all.isnull().values.any())

sensor_pre.rename(columns = {'value':'target'}, inplace = True) 
source_one_pre.rename(columns = {'value':'value_one'}, inplace = True) 
source_two_pre.rename(columns = {'value':'value_two'}, inplace = True) 


temp_merge = pd.merge(sensor_pre[:8760], source_one_pre, on='datetime')
sensor_all_pre = pd.merge(temp_merge, source_two_pre, on='datetime')
sensor_all_pre['month'] = pd.DatetimeIndex(sensor_pre['datetime']).month

"Any missing values : " +  str(sensor_all_pre.isnull().values.any())


sensor_hum.rename(columns = {'value':'target'}, inplace = True) 
source_one_hum.rename(columns = {'value':'value_one'}, inplace = True) 
source_two_hum.rename(columns = {'value':'value_two'}, inplace = True) 


temp_merge = pd.merge(sensor_hum, source_one_hum, on='datetime')
sensor_all_hum = pd.merge(temp_merge, source_two_hum, on='datetime')
sensor_all_hum['month'] = pd.DatetimeIndex(sensor_hum['datetime']).month

"Any missing values : " +  str(sensor_all_hum.isnull().values.any())


sensor_all.to_csv("sensor_all.csv")
sensor_all_hum.to_csv("sensor_all_hum.csv")
sensor_all_pre.to_csv("sensor_all_pre.csv")


#
# Azure ml
# 
ws = Workspace.get(name='MLN',
                   subscription_id='badcc2bf-a4d3-4b35-9d81-5bc289cd48e3',
                   resource_group='MLR')

default_ds = ws.get_default_datastore()


default_ds.upload_files(files=['./sensor_all.csv', './sensor_all_hum.csv', './sensor_all_pre.csv'], # Upload the diabetes csv files in /data
                       target_path='sensor-data/', # Put it in a folder path in the datastore
                       overwrite=True, # Replace existing files of the same name
                       show_progress=True)


