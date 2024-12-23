# Path setup, and access the config.yml file, datasets folder & trained models
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Dict, List
from pydantic import BaseModel
from strictyaml import YAML, load

import model

# Project Directories
PACKAGE_ROOT = Path(model.__file__).resolve().parent
#print(PACKAGE_ROOT)
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
#print(CONFIG_FILE_PATH)

DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    training_data_file: str
    test_data_file: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """
    target: str
    features: List[str]
    
    cols_delete: List[str]
    
    age_binner: List[str]
    age_bins: List[int]
    age_bin_labels: List[str]
    
    mapping_dict: Dict[str, Dict[int, int]]
    
    num_cols: List[str]
    
    balance_binner: List[str]
    bal_bins: List[int]
    bal_bin_labels: List[str]
    
    tenure_binner: List[str]
    ten_bins: List[int]
    ten_bin_labels: List[str]
    
    onehot_cols: List[str]
    label_cols: List[str]
  
    test_size:float
    random_state: int
    n_estimators: int
    max_depth: int
    learning_rate: float
    loss_function: str
    auto_class_weights: str
    verbose: int

class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    modl_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        modl_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()