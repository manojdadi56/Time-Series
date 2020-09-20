import json
import joblib
import numpy as np
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path('outputs/model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    predictions = model.forecast(data)
    return json.dumps({"Time":str(predictions.index[0]), "prediction": predictions[0]})
