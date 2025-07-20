import boto3
from botocore.exceptions import ClientError
from django.conf import settings # A.settings.py
import logging

class Bucket:
    """
    CDN bucket manager
    
    init method creates connection.
    
    NOTE:
        none of these methods are async. use public interface in task.py module instead.
    """
    def __init__(self):
        try:
            self.s3_resource = boto3.resource(
                service_name=settings.AWS_S3_SIGNATURE_VERSION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL
            )
        except Exception as exc:
            logging.error(exc)
    
    def get_objects(self):
        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            bucket = self.s3_resource.Bucket(bucket_name)
            objects = bucket.objects.all()
            if not objects:
                logging.info(f"No objects found in bucket: {bucket_name}")
                return None
            return objects
        except ClientError as e:
            logging.error(e)
    
    def delete_object(self, key):
        self.s3_resource.meta.client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key
        )
        return True
    
    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).download_fileobj(key, f)
    
    def upload_object(self, file, obj_name):
        self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            ACL='private',
            Body=file,
            Key=obj_name
        )

bucket = Bucket()