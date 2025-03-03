import boto3
import os
import config


class S3BucketCleaner:
    def __init__(self):
        self.target_region = config.REGION
        self.prefix = config.PREFIX
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')

    def list_buckets(self):
        try:
            return self.s3_client.list_buckets().get('Buckets', [])
        except Exception as e:
            print(f"Failed to retrieve bucket list: {e}")
            return []

    def get_bucket_location(self, bucket_name):
        try:
            location = self.s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            return 'us-east-1' if location is None else location
        except Exception as e:
            print(f"Failed to retrieve region for bucket {bucket_name}: {e}")
            return None

    def empty_bucket(self, bucket_name):
        print(f"---empty bucket: {bucket_name}")
        bucket_resource = self.s3_resource.Bucket(bucket_name)
        try:
            print(f"---Deleted regular objects in {bucket_name}: {bucket_resource.objects.all().delete()}")
        except Exception as e:
            print(f"Failed to delete regular objects in bucket {bucket_name}: {e}")
        try:
            print(f"---Deleted versioned objects in {bucket_name}: {bucket_resource.object_versions.delete()}")
        except Exception as e:
            print(f"Failed to delete versioned objects in bucket {bucket_name}: {e}")

    def delete_bucket(self, bucket_name):
        print(f"---Attempting to delete bucket: {bucket_name}")
        try:
            print(f"---Bucket {bucket_name} deleted successfully: {self.s3_client.delete_bucket(Bucket=bucket_name)}")
        except Exception as e:
            print(f"Failed to delete bucket {bucket_name}: {e}")

    def delete_specific_buckets(self):
        for bucket in self.list_buckets():
            bucket_name = bucket['Name']
            location = self.get_bucket_location(bucket_name)
            if location and location in self.target_region:
                if any(bucket_name.startswith(prefix) for prefix in self.prefix):
                    print(f"---Deleting bucket: {bucket_name}")
                    self.empty_bucket(bucket_name)
                    self.delete_bucket(bucket_name)
                else:
                    print(f"\nBucket {bucket_name} does not match the prefix criteria, skipping deletion.")
            else:
                print(f"\nBucket {bucket_name}/{location} does not match the target region, skipping.")

    def retain_specific_bucket(self):
        for bucket in self.list_buckets():
            bucket_name = bucket['Name']
            location = self.get_bucket_location(bucket_name)
            if location and location in self.target_region:
                if any(bucket_name.startswith(prefix) for prefix in self.prefix):
                    print(f"\nRetaining bucket: {bucket_name}")
                else:
                    print(f"\nProcessing bucket for deletion (not retained): {bucket_name}")
                    self.empty_bucket(bucket_name)
                    self.delete_bucket(bucket_name)
            else:
                print(f"\nBucket {bucket_name}/{location} does not match the target region, skipping deletion.")

        
def lambda_handler(event, context):
    cleaner = S3BucketCleaner()
    if config.BUCKET_PROCESSING.upper() == "RETAIN":
        cleaner.retain_specific_bucket()
    elif config.BUCKET_PROCESSING.upper() == "DELETE":
        cleaner.delete_specific_buckets()
    else:
        print(f"Invalid BUCKET_PROCESSING value: {config.BUCKET_PROCESSING}. You must set BUCKET_PROCESSING to either RETAIN or DELETE")