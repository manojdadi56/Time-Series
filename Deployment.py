from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
from azureml.core import Model
from azureml.core import Workspace

ws = Workspace.from_config()

for model in Model.list(ws):
    print(model.name, 'version:', model.version)
    for tag_name in model.tags:
        tag = model.tags[tag_name]
        print ('\t',tag_name, ':', tag)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    print('\n')

service_name = "sensor-service7"

# Configure the scoring environment
inference_config = InferenceConfig(runtime= "python",
                                   source_directory = './',
                                   entry_script="./Prediction.py",
                                   conda_file="./Outputs/conda_env.yml")

deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)

service = Model.deploy(ws, service_name, [model], inference_config, deployment_config)
