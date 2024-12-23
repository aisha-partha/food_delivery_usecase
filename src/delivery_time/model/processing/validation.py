import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError
import datetime

from model.config.core import config
from model.processing.data_manager import load_dataset


def validate_inputs(*, input_df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    
    dataframe = input_df
    validated_data = dataframe[config.modl_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    
    customer_id: Optional[int]
    credit_score: Optional[int]
    country: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    tenure: Optional[int]
    balance: Optional[float]
    products_number: Optional[int]
    credit_card: Optional[int]
    active_member: Optional[int]
    estimated_salary: Optional[float]
    
class MultipleDataInputs(BaseModel):
    
    inputs: List[DataInputSchema]