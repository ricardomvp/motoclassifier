#Standard libraries
import os
#aws
import boto3

def upload_to_aws(img):
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    S3_BUCKET = os.environ.get('S3_BUCKET')

    s3.upload_fileobj(img, S3_BUCKET,'images/'+img.name, ExtraArgs={ "ContentType": "image/jpeg",
                                                                     'ACL':'public-read'})
