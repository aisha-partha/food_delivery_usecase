import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Union
import pandas as pd
import numpy as np

from model import __version__ as _version
from model.config.core import config
from model.pipeline import bank_pipe
from model.processing.data_manager import load_pipeline
from model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
bank_pipe= load_pipeline(file_name=pipeline_file_name)


def make_prediction(*,input_data:Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model """

    validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    
    try:
        
        validated_data=validated_data.reindex(columns=config.modl_config.features)
        #print(validated_data)
    
    except Exception as e:
        return e
    
    results = {"predictions": None, "version": _version, "errors": errors}
    
    predictions = bank_pipe.predict(validated_data)

    results = {"predictions": predictions,"version": _version, "errors": errors}
    print(results)
    
    if not errors:

        predictions = bank_pipe.predict(validated_data)
        results = {"predictions": predictions,"version": _version, "errors": errors}
        #print(results)

    return results

if __name__ == "__main__":

    data_in={'customer_id': [15584532],
             'credit_score': [709],
             'country': ['France'],
             'gender': ['Female'],
             'age': [36],
             'tenure': [7],
             'balance': [0],
             'products_number': [1],
             'credit_card': [0],
             'active_member': [1],
             'estimated_salary': [42085.58]
    }
    
    make_prediction(input_data=data_in)
