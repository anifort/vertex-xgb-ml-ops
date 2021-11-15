import pipeline
from argparse import ArgumentParser
from google.cloud.aiplatform.pipeline_jobs import PipelineJob
import json
'''

example: 
python3 run-pipeline.py -uri gs://feature-store-mars21/test/pipeline.json -l us-central1 -pp '{"project_id": "feature-store-mars21",   "data_path": "gs://mortgage_dataset_files/mortgage-small.csv"}' -pn my-test -pid feature-store-mars21 -ruri gs/feature-store-mars21/test -rn my-test-r1




client=KfpClient(
    host="https://kubeflow-oct.endpoints.myfirstproject-226013.cloud.goog/pipeline",
    client_id="478111835512-94l3kca44ueiudgm9tr2ibg4ihah5g3d.apps.googleusercontent.com");

client.create_pipeline_version(
    pipeline_id="1234",
    name="$COMMIT_SHA",
    repo_name="$REPO_NAME",
    commit_sha="$COMMIT_SHA",
    url="https://storage.googleapis.com/$REPO_NAME/$COMMIT_SHA/pipeline.zip")

'''
def run_pipeline(pipeline_name, run_name, project_id, pl_root, pl_path, location, pipeline_params):
    pl = PipelineJob(
        enable_caching=True,
        display_name = pipeline_name,
        job_id = run_name,
        pipeline_root=pl_root,
        template_path = pl_path,
        project = project_id,
        location = location,
        parameter_values = pipeline_params)

    status = pl.run(sync=True)
    
    if(pl.has_failed):
        exit(1)
    
    


'''

`state="PIPELINE_STATE_SUCCEEDED" AND display_name="my_pipeline"``
            -  ``state="PIPELINE_STATE_RUNNING" OR display_name="my_pipeline"``
            -  ``NOT display_name="my_pipeline"``
            
            
example: 
python3 run-pipeline.py -uri gs://feature-store-mars21/test/pipeline.json -l us-central1 -pp '{"project_id": "feature-store-mars21",   "data_path": "gs://mortgage_dataset_files/mortgage-small.csv"}' -pn my-test -pid feature-store-mars21 -ruri gs://feature-store-mars21/test -rn my-test-r1

'''

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-pn", "--pipeline_name",
                        dest="pipeline_name",
                        default="$REPO_NAME",
                        help="")
    
    parser.add_argument("-rn", "--run_name",
                        dest="run_name",
                        default="$SHORT_SHA",
                        help="")
    
       
    parser.add_argument("-pid", "--project_id",
                        dest="project_id",
                        default="$PROJECT_ID",
                        help="")
    
       
    parser.add_argument("-ruri", "--pipeline_root_uri",
                        dest="pipeline_root_uri",
                        required=True,
                        help="")
    
       
    parser.add_argument("-uri", "--pipeline_gs_path",
                        dest="pipeline_gs_path",
                        required=True,
                        help="")
       
    parser.add_argument("-l", "--location",
                        dest="location",
                        default="us-central1",
                        required=True,
                        help="")
       
    parser.add_argument("-pp", "--pipeline_params",
                        dest="pipeline_params",
                        default="{}",
                        required=True,
                        help="json string of pipelines params")

    
    args = parser.parse_args()
    
    
    print(vars(args))
    run_pipeline(
        args.pipeline_name,
        args.run_name,
        args.project_id,
        args.pipeline_root_uri,
        args.pipeline_gs_path,
        args.location,
        json.loads(args.pipeline_params))