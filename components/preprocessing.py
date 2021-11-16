from kfp.v2.dsl import (
    component,
    Output,
    Dataset
)
from kfp import components

@component( 
    packages_to_install=['argparse','pandas','xgboost','numpy','sklearn','fsspec','gcsfs'], 
    base_image='python:3.9',
    output_component_file='preprocess.yaml',
    #target_image='gcr.io/feature-strore-mars21/sklearn-pipeline/preprocess'
)
def split_data(
    data_out_x_train: Output[Dataset],
    data_out_x_test: Output[Dataset],
    data_out_y_train: Output[Dataset],
    data_out_y_test: Output[Dataset],
    data_path: str,
):
    import pandas as pd
    import xgboost as xgb
    import numpy as np
    import collections
    import sklearn
    from google.cloud import storage # test
    from sklearn.model_selection import train_test_split
    from sklearn.utils import shuffle

    ### Import data ###
    COLUMN_NAMES = collections.OrderedDict({
        'as_of_year': np.int16,
        'agency_code': 'category',
        'loan_type': 'category',
        'property_type': 'category',
        'loan_purpose': 'category',
        'occupancy': np.int8,
        'loan_amt_thousands': np.float64,
        'preapproval': 'category',
        'county_code': np.float64,
        'applicant_income_thousands': np.float64,
        'purchaser_type': 'category',
        'hoepa_status': 'category',
        'lien_status': 'category',
        'population': np.float64,
        'ffiec_median_fam_income': np.float64,
        'tract_to_msa_income_pct': np.float64,
        'num_owner_occupied_units': np.float64,
        'num_1_to_4_family_units': np.float64,
        'approved': np.int8
    })

    data = pd.read_csv(data_path, index_col=False, dtype=COLUMN_NAMES)
    
    ### Feature engineering ###
    data = data.dropna()
    data = data[0:100]
    data = shuffle(data, random_state=2)

    labels = data['approved'].values
    data = data.drop(columns=['approved'])

    dummy_columns = list(data.dtypes[data.dtypes == 'category'].index)
    data = pd.get_dummies(data, columns=dummy_columns)

    x,y = data.values,labels
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    
    ### Export data as artifact ###
    pd.DataFrame(x_train).to_csv(data_out_x_train.path, index=False, header=False)  
    pd.DataFrame(y_train).to_csv(data_out_y_train.path, index=False, header=False)  
    pd.DataFrame(x_test).to_csv(data_out_x_test.path, index=False, header=False)  
    pd.DataFrame(y_test).to_csv(data_out_y_test.path, index=False, header=False)