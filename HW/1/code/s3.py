import boto3, logging, os, io
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


def s3_config():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    s3_resource = None
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('S3_AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('S3_AWS_SECRET_ACCESS_KEY')
        )
        return s3_resource
    except Exception as exc:
        logging.error(exc)


def s3_put_object(user_object, object_name):
    s3_resource = s3_config()
    try:
        bucket = s3_resource.Bucket('coderunner')
        bucket.put_object(
            ACL='private',
            Body=user_object,
            Key=object_name
        )
        return True
    except ClientError as e:
        print(e)
        raise "code uploading at s3 failed."


def s3_download_object(object_name):
    s3_resource = s3_config()
    try:

        response = s3_resource.Object("coderunner", object_name).get()
        code=response['Body'].read().decode()
        return code
    except ClientError as e:
        print(e)
        raise "code downloading failed."



