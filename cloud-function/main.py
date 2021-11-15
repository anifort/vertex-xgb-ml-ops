import base64

from google.cloud.aiplatform.pipeline_jobs import PipelineJob


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
        job_id = "schedule-run-a3b8252-"+"".join(e for e in str(context.timestamp) if e.isalnum()),
        pipeline_root="gs://feature-store-mars21/vertex-xgb-ml-ops/a3b8252",
        template_path = "gs://feature-store-mars21/vertex-xgb-ml-ops/a3b8252/pipeline.json",
        project = "feature-store-mars21",
        location = "us-central1",
        parameter_values = {"project_id":"feature-store-mars21","data_path":"gs://mortgage_dataset_files/mortgage-small.csv"})

    pl.run(sync=False, service_account="pipelines-cloud-build@feature-store-mars21.iam.gserviceaccount.com")
   
