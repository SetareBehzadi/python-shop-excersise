from django.conf import settings
import boto3
import logging


class Bucket:

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.s3_resource = boto3.resource(
            service_name=settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def get_objects_v1(self):
        result = self.conn.list_objects_v2(Bucket=self.bucket_name)
        if result['KeyCount']:
            res = result['Contents']
        else:
            res = None
        return res

    def get_objects_v2(self):
        bucket = self.s3_resource.Bucket(self.bucket_name)
        result = bucket.objects.all()
        size = sum(1 for _ in bucket.objects.all())
        if size :
            for obj in bucket.objects.all():
                print("dddd" * 9)
                print(f"object_name: {obj.key}, last_modified: {obj.last_modified}")
        print(bucket.objects.all())



    def delete_object_v2(self, object_name):
        bucket = self.s3_resource.Bucket(self.bucket_name)
        object = bucket.Object(object_name)

        return object.delete(
            VersionId='string',
        )

    def delete_object(self, key):
        self.conn.delete_object(Bucket=self.bucket_name, Key=key)
        return True

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(self.bucket_name, key, f)


buckets = Bucket()
