from kfp.v2 import compiler
import pipeline, deploy_model_pipeline
from google.cloud import storage
import os

from argparse import ArgumentParser


def compile(pipeline, pipeline_filename):
    if pipeline=='deploy-model':
        pipeline_function = deploy_model_pipeline.deploy_model_xgb_pipeline
    else:
        pipeline_function = pipeline.xgb_pipeline
     
    compiler.Compiler().compile(
        pipeline_func=pipeline_function,
        package_path=pipeline_filename
    )


def upload(destination, pipeline_filename):
    uri = destination[5:]
    uri_parts = uri.split("/")
    bucket_name = uri_parts[0]
    source_blob_name = "/".join(uri_parts[1:])

    blob = storage.Client().bucket(bucket_name).blob("/".join(uri_parts[1:]))
    blob.upload_from_filename(pipeline_filename)
    

'''
example:
python3 compile-pipeline.py -d gs://feature-store-mars21/test/pipeline.json
'''
if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("-d", "--dest",
                        dest="destination",
                        required=True,
                        help="gs:// path to export pipeline including the archived name and extension")
    
    parser.add_argument("-pt", '--pipeline-type',
                    choices=['training','deploy-model'],
                    default='training',
                    help='define pipeline type')

    args = parser.parse_args()
    
    
    pipeline_filename='pipeline.json' 

    compile(args.pipeline_type, pipeline_filename)
    upload(args.destination, pipeline_filename)