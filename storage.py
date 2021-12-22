import boto3
import os
from botocore.exceptions import ClientError

# move to interface (can i do this in python?)
def upload_to_storage(file_name: str):
    object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3', endpoint_url='https://gateway.eu1.storjshare.io')

    try:
        response = s3_client.upload_file(file_name, "yt-videos", object_name)
    except ClientError as e:
        print(e)
        return False
    return True