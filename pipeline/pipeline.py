import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import kfp.v2 as kfp
import kfp.v2.dsl as dsl
from kfp.v2 import compiler
from kfp.v2.google.client import AIPlatformClient
from google_cloud_pipeline_components import aiplatform as gcc_aip

from components.preprocessing import split_data
from components.training import xgb_training


@dsl.pipeline(
  name='xgb-pipeline',
  description='pipeline training an xgb model',
)
def pipeline(
    data_path: str,
    project_id: str,
    endpoint_name: str = 'xgb-ep'
):
    
    prepro_op = split_data(data_path)
    
    
    train_op = xgb_training(
        prepro_op.outputs['data_out_x_train'],
        prepro_op.outputs['data_out_y_train'],
        prepro_op.outputs['data_out_x_test'],
        prepro_op.outputs['data_out_y_test']
    )
    train_op.set_cpu_limit('4')
    train_op.set_memory_limit('14Gi')
    #train_op.add_node_selector_constraint('cloud.google.com/gke-accelerator', 'nvidia-tesla-k80')
    #train_op.set_gpu_limit(1)
    
    ### Create endpoint
    endpoint_create_op = gcc_aip.EndpointCreateOp(
        project=project_id,
        display_name=endpoint_name
    ).after(train_op)
    
    
    ### Use predefined component to upload model
    model_upload_op = gcc_aip.ModelUploadOp(
        project=project_id,
        display_name='modelxgb',
        artifact_uri=train_op.outputs["path"],
        serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-4:latest'
    ).after(train_op)
    
    
    #deploy_op = gcc_aip.ModelDeployOp(  
    #    model=train_op.outputs["model"],
    #)
    
    custom_model_deploy_op = gcc_aip.ModelDeployOp(
       endpoint=endpoint_create_op.outputs["endpoint"],
        model=model_upload_op.outputs["model"],
        dedicated_resources_machine_type="n1-standard-4",
        dedicated_resources_min_replica_count=1
    )
    
'''   
compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path="pl.json"
)


from google.cloud.aiplatform.pipeline_jobs import PipelineJob

pl = PipelineJob(display_name= 'xgb-job',
        pipeline_root=""
        template_path= "pl.json",
        location='us-central1',
        parameter_values={'project_id': 'feature-store-mars21', 
                          'data_path': 'gs://mortgage_dataset_files/mortgage-small.csv'})

pl.run(sync=False)'''