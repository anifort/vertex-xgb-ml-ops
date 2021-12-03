import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import kfp.v2 as kfp
import kfp.v2.dsl as dsl
from kfp.v2 import compiler

from google_cloud_pipeline_components import aiplatform as gcc_aip

from components.metadata import metadata_model_search


@dsl.pipeline(
  name='deploy-model-xgb-pipeline',
  description='pipeline training an xgb model',
)
def deploy_model_xgb_pipeline(
    project_id: str,
    region: str,
    metadata_name: str,
    model_uri_path: str,
    endpoint_name: str = 'xgb-ep'
):
    
    model_op = metadata_model_search(
        project_id,
        region,
        metadata_name,
        model_uri_path)
      
    
    ### Create endpoint
    endpoint_create_op = gcc_aip.EndpointCreateOp(
        project=project_id,
        display_name=endpoint_name
    ).after(model_op)
    
    
    ### Use predefined component to upload model
    model_upload_op = gcc_aip.ModelUploadOp(
        project=project_id,
        display_name='modelxgb',
        artifact_uri=model_op.output,
        serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-4:latest'
    ).after(model_op)
    
    custom_model_deploy_op = gcc_aip.ModelDeployOp(
       endpoint=endpoint_create_op.outputs["endpoint"],
        model=model_upload_op.outputs["model"],
        dedicated_resources_machine_type="n1-standard-4",
        dedicated_resources_min_replica_count=1
    )
    
