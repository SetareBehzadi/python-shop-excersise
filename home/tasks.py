from bucket import buckets
from celery import shared_task


def all_buckets_objects_task():
    res = buckets.get_objects_v1() # behtar va khanatar ast
    # buckets.get_objects_v2()
    return res


@shared_task
def delete_object_ask(key):
    buckets.delete_object(key)


@shared_task
def download_object_task(key):
    buckets.download_object(key)

