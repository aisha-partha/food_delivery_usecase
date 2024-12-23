from typing import Any, List, Optional

from pydantic import BaseModel
from model.processing.validation import DataInputSchema

class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    #predictions: Optional[List[int]]
    predictions: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        'customer_id': 15584532,
                        'credit_score': 709,
                        'country': 'France',
                        'gender': 'Female',
                        'age': 36,
                        'tenure': 7,
                        'balance': 0,
                        'products_number': 1,
                        'credit_card': 0,
                        'active_member': 1,
                        'estimated_salary': 42085.58
                    }
                ]
            }
        }
