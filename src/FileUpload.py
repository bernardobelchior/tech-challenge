import boto3
from botocore.client import Config

BUCKET_NAME="wacky-assets"

class FileUpload():
    def __init__(self): 
       self.s3 = boto3.client("s3", config=Config(signature_version='s3v4'), aws_access_key_id="ACCESS_KEY_ID", aws_secret_access_key="SECRET_ACCESS_KEY") # needs to use s3v4 because germany is secure ;)
       print(self.s3.list_buckets())

    def upload_file(self, name, content):
        response = self.s3.put_object(Bucket=BUCKET_NAME, Key=name, Body=content, ACL='public-read')

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Upload failed")

        return "https://s3.eu-central-1.amazonaws.com/{}/{}".format(BUCKET_NAME, name)
