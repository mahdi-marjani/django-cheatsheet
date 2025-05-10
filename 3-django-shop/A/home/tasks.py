from bucket import bucket


# TODO: Should be made async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result