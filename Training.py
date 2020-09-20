# Import libraries
from azureml.core import Run
import argparse
import pandas as pd
import joblib
import statsmodels.api as sm

# Get parameters
parser = argparse.ArgumentParser()
parser.add_argument('--order', type=str, dest='order', default=(0,0,1))
parser.add_argument('--seasonal_order', type=str, dest='seasonal_order', default=(0,0,1,24))
args = parser.parse_args()
order = eval(args.order)
seasonal_order = eval(args.seasonal_order)

# Get the experiment run context
run = Run.get_context()

# Get sensor data
sensor_all = run.input_datasets['sensor_all'].to_pandas_dataframe()

# Prepare for training 
exog_data  = sensor_all[["value_one", "value_two", "month", "datetime"]].set_index('datetime')
endog = sensor_all[["target", "datetime"]].set_index('datetime') 

# Model
mod = sm.tsa.statespace.SARIMAX(endog= endog,
                                exog = exog_data,
                                order=order,
                                seasonal_order=seasonal_order,
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print('SARIMA{}x{} - AIC:{}'.format(order, seasonal_order, results.aic))


results.save('model.pkl')
run.upload_file(name = 'Outputs/model.pkl', path_or_stream = './model.pkl')

# Register the model
run.register_model(model_path='Outputs/model.pkl', model_name='sensor_model_1',
                   tags={'Training context':'Inline Training'},
                   properties={'AUC': results.aic})


# Log metrics
run.log('seasonal_order', str(seasonal_order))
run.log('order', str(order))
run.log('aic', str(results.aic))


run.complete()
