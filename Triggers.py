from azureml.train.estimator import Estimator
from azureml.core import Environment, Experiment
from azureml.widgets import RunDetails
from azureml.core import Dataset
from azureml.core import Workspace

#
# Azure ml
#

ws = Workspace.from_config()

for ct_name in ws.compute_targets:
    print(ct_name)


experiment_folder = 'sensor_datastore'

default_ds = ws.get_default_datastore()


# Get the environment
registered_env = Environment.get(ws, 'sensor-experiment-env')

# Set the script parameters
script_params = {'--order': '(2, 1, 2)', '--seasonal_order': '(2, 1, 2, 24)'}

# Get the training dataset
sensor_all = Dataset.Tabular.from_delimited_files(path=(default_ds, 'sensor-data/sensor_all.csv'))

# Create an estimator
estimator = Estimator(source_directory="./",
                      inputs=[sensor_all.as_named_input('sensor_all')],
                      script_params = script_params,
                      compute_target = ct_name, # Run the experiment on the remote compute target
                      environment_definition = registered_env,
                      entry_script='./Training.py')

# Create an experiment
experiment = Experiment(workspace = ws, name = 'sensor-training')

# Run the experiment
run = experiment.submit(config=estimator)
# Show the run details while running
RunDetails(run).show()
run.wait_for_completion()




