from bucket import bucket
from celery import shared_task
import os


# TODO: Should be made async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result

@shared_task
def delete_object_task(key):
    bucket.delete_object(key)
    
@shared_task
def download_object_task(key):
    bucket.download_object(key)

@shared_task
def upload_object_task(filepath, obj_name):
    with open(filepath, "rb") as f:
        bucket.upload_object(f, obj_name)
    os.remove(filepath)
