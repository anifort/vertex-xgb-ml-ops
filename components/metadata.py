from kfp.v2.dsl import (
    component,
    Output,
    Dataset
)
from kfp import components

@component( 
    packages_to_install=['google-cloud-aiplatform','pandas'], 
    base_image='python:3.9',
    #output_component_file='preprocess.yaml',
    #target_image='gcr.io/feature-strore-mars21/sklearn-pipeline/preprocess'
)
def metadata_model_search(
    project_id: str,
    region: str,
    metadata_name: str,
    model_uri_path: str
) -> str:
        
    from google.cloud import aiplatform_v1 
    import pandas as pd

    metadata_client = aiplatform_v1.MetadataServiceClient(
      client_options={
          "api_endpoint": "{}-aiplatform.googleapis.com".format(region)
      }
    )
    if not model_uri_path.endswith("/"):
        model_uri_path+='/'
    MODEL_FILTER="uri = \"{}*\" AND schema_title=\"system.Model\"".format(model_uri_path)
    PARENT="projects/{0}/locations/{1}/metadataStores/{2}".format(project_id, region, metadata_name)
    artifact_request = aiplatform_v1.ListArtifactsRequest(
        parent=PARENT,
        filter=MODEL_FILTER
    )
    model_artifacts = metadata_client.list_artifacts(artifact_request)

    time_last=None
    uri_last =None
    for ma in model_artifacts:
        print(ma)
        if uri_last==None:
            uri_last=ma.uri
            time_last=ma.create_time
        elif(time_last<ma.create_time):
            uri_last=ma.uri
            time_last=ma.create_time
            
    if uri_last is None:
        raise Exception('model uri not found')   
        
    return uri_last

    
    