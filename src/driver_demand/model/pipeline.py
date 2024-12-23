import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostClassifier, metrics

from model.config.core import config
from model.processing.features import *



bank_pipe = Pipeline([

    ## Unused columns ##
    ('unused_column_dropper', ColumnDropper(config.modl_config.cols_delete)),

    ## Binning age variable ##
    ('age_binner', Binner(config.modl_config.age_binner, config.modl_config.age_bins, 
                          config.modl_config.age_bin_labels)),

    ## Mapping ##
    ('all_mapper', Mapper(config.modl_config.mapping_dict)),

    ## Outlier handling ##
    ('all_outlier', OutlierHandler(config.modl_config.num_cols)),
    
    ## Binning age variable ##
    ('balance_binner', Binner(config.modl_config.balance_binner, config.modl_config.bal_bins, 
                              config.modl_config.bal_bin_labels)),

    ## Binning tenure variable ##
    ('tenure_binner', Binner(config.modl_config.tenure_binner, config.modl_config.ten_bins, 
                             config.modl_config.ten_bin_labels)),
    
    ## One hot encoder ##
    ('one_hot_encoder', ColOneHotEncoder(config.modl_config.onehot_cols)),

    ## Label encoder ##
    ('label_encoder', ColLabelEncoder(config.modl_config.label_cols)),
     
    ## scaler ##
    ('scaler', StandardScaler()),

    ## Model fit
    ('model_cb', CatBoostClassifier(n_estimators=config.modl_config.n_estimators, 
                                    max_depth=config.modl_config.max_depth, 
                                    learning_rate=config.modl_config.learning_rate, 
                                    loss_function=config.modl_config.loss_function, 
                                    auto_class_weights=config.modl_config.auto_class_weights,
                                    random_state=config.modl_config.random_state, 
                                    verbose=config.modl_config.verbose))
])