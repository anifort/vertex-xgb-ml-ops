import base64

def pipeline_trigger(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    
    
    # get gcs path for pub/sub msg
    # read file from gcs
    # get configs from file and use the below
    
    #pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    #print(pubsub_message)
    pl = PipelineJob(
        enable_caching=True,
        display_name = "xgb-pipeline",
        job_id = "run-a3b8252",
        pipeline_root="gs://feature-store-mars21/vertex-xgb-ml-ops/a3b8252",
        template_path = "gs://feature-store-mars21/vertex-xgb-ml-ops/a3b8252/pipeline.json",
        project = "feature-store-mars21",
        location = "us-central1",
        parameter_values = {"project_id":"feature-store-mars21","data_path":"gs://mortgage_dataset_files/mortgage-small.csv"})

    status = pl.run(sync=False, service_account="pipelines-cloud-build@feature-store-mars21.iam.gserviceaccount.com")
    
    if(pl.has_failed):
        exit(1)