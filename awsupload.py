import boto3
from botocore.client import Config


s3 = boto3.client("s3", aws_access_key_id="AKIAICSCFYPWBK26YROQ", aws_secret_access_key="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",
			config=Config(signature_version='s3v4'))    # needs to use s3v4 because germany is secure ;)

# get buckets
response = s3.list_buckets()


# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
s3.upload_file("./test.py", "wackypics", "testup")

