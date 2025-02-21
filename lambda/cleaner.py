import boto3
import os
import config as config


class S3BucketCleaner:
    def __init__(self, target_region, prefix):
        self.target_region = target_region
        self.prefix = prefix
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.region = config.REGION
        self.prefix = config.PREFIX

    def list_buckets(self):
        """List all buckets"""
        try:
            buckets_response = self.s3_client.list_buckets()
            return buckets_response.get('Buckets', [])
        except Exception as e:
            print(f"Failed to retrieve bucket list: {e}")
            return []

    def get_bucket_location(self, bucket_name):
        """Get the region of the bucket. If it is us-east-1, it might return None; in that case, treat it as 'us-east-1'."""
        try:
            location = self.s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            return 'us-east-1' if location is None else location
        except Exception as e:
            print(f"Failed to retrieve region for bucket {bucket_name}: {e}")
            return None

    def empty_bucket(self, bucket_name):
        """Empty all regular objects and versioned objects in the specified bucket"""
        print(f"Starting to empty bucket: {bucket_name}")
        bucket_resource = self.s3_resource.Bucket(bucket_name)
        try:
            # Delete all regular objects
            delete_objects = bucket_resource.objects.all().delete()
            print(f"Deleted regular objects in {bucket_name}: {delete_objects}")
        except Exception as e:
            print(f"Failed to delete regular objects in bucket {bucket_name}: {e}")
        try:
            # Delete all versioned objects (for buckets with versioning enabled)
            delete_versions = bucket_resource.object_versions.delete()
            print(f"Deleted versioned objects in {bucket_name}: {delete_versions}")
        except Exception as e:
            print(f"Failed to delete versioned objects in bucket {bucket_name}: {e}")
        print(f"Bucket {bucket_name} has been emptied.")

    def delete_bucket(self, bucket_name):
        """Delete the specified bucket. The bucket must be empty."""
        print(f"Attempting to delete bucket: {bucket_name}")
        try:
            response = self.s3_client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully: {response}")
        except Exception as e:
            print(f"Failed to delete bucket {bucket_name}: {e}")

    def process_buckets(self):
        """
        Process all buckets:
          1. Operate only on buckets whose names start with the specified prefix.
          2. Check if the bucket's region matches the target region; if so, empty it and then delete the bucket.
        """
        buckets = self.list_buckets()
        for bucket in buckets:
            bucket_name = bucket['Name']
            # Filter based on bucket name prefix
            if not bucket_name.startswith(self.prefix):
                print(f"Bucket {bucket_name} does not meet the criteria (prefix: {self.prefix}), skipping.")
                continue

            location = self.get_bucket_location(bucket_name)
            if location is None:
                continue

            if location == self.target_region:
                print(f"Processing bucket: {bucket_name}")
                self.empty_bucket(bucket_name)
                self.delete_bucket(bucket_name)
            else:
                print(f"Bucket {bucket_name} is in region ({location}) which does not match the target region {self.target_region}, skipping.")

def lambda_handler(event, context):
    # Retrieve the target region from environment variables, or use config as default (e.g., "us-east-1")
    region = os.environ.get('TARGET_REGION', config.REGION)
    # Specify the bucket name prefix; only process buckets whose names start with the specified prefix
    prefix = os.environ.get('PREFIX', config.PREFIX)
    cleaner = S3BucketCleaner(target_region=region, prefix=prefix)
    cleaner.process_buckets()