from kfp.v2.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Metrics,
    Model,
    ClassificationMetrics
)

from typing import NamedTuple

@component(
    packages_to_install=['argparse','pandas','xgboost','numpy','sklearn','fsspec','gcsfs'], 
    base_image='python:3.9',
    output_component_file='train.yaml',
    #target_image='gcr.io/feature-strore-mars21/sklearn-pipeline/train')
)
def xgb_training( 
    dta_in_x_train: Input[Dataset], 
    dta_in_y_train: Input[Dataset],
    dta_in_x_test: Input[Dataset],
    dta_in_y_test: Input[Dataset],
    model: Output[Model],
    metrics_conf: Output[ClassificationMetrics],
    metrics_para: Output[Metrics]
)  -> NamedTuple(
    'ModelPathOut',
    [
      ('path', str)
    ]):
    
    import pandas as pd
    import xgboost as xgb
    import numpy as np
    from google.cloud import storage
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_curve
    import os
    
    from collections import namedtuple
    
    ### Load data ###
    x_train = pd.read_csv(dta_in_x_train.path, header=None)
    y_train = pd.read_csv(dta_in_y_train.path, header=None)
    x_test = pd.read_csv(dta_in_x_test.path, header=None)
    y_test = pd.read_csv(dta_in_y_test.path, header=None)
    
    ### Build model ###
    eval_set = [(x_train, y_train.values.ravel()), (x_test, y_test.values.ravel())]
    eval_metric = ["auc"]
    bst = xgb.XGBClassifier(objective='reg:logistic')
    bst.fit(x_train, y_train.values.ravel(), eval_set=eval_set, eval_metric=eval_metric)
        
    ### Create evaluation metrics ###
        # Confusion matrix
    pred = bst.predict(x_train)
    metrics_conf.log_confusion_matrix(["0", "1"], confusion_matrix(y_train.values.ravel(), pred).tolist())
    
        # Additional metrics
    results = bst.evals_result()
    auc = results['validation_0']['auc'][0]
    metrics_para.log_metric("auc", (auc))
    
    ### Export model ###
    os.makedirs(model.path, exist_ok=True)
    bst.save_model(model.path+"/model.bst")
    
    output = namedtuple('ModelPathOut',
        ['path'])
    return output(model.path.replace('/gcs/', 'gs://'))