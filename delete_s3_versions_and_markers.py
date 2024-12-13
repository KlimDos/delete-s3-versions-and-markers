import os
import boto3
from botocore.exceptions import ClientError
import argparse

# Initialize S3 client
s3_client = boto3.client('s3')

def delete_objects(bucket_name, objects_to_delete):
    """
    Delete a batch of objects from the S3 bucket.
    
    Args:
    bucket_name (str): Name of the S3 bucket.
    objects_to_delete (list): List of dictionaries containing 'Key' and 'VersionId' of objects to delete.
    
    Returns:
    int: Number of successfully deleted objects.
    """
    if not objects_to_delete:
        return 0

    try:
        response = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )
        deleted_count = len(response.get('Deleted', []))
        errors = response.get('Errors', [])
        
        if errors:
            print(f"Encountered {len(errors)} errors while deleting objects.")
            for error in errors:
                print(f"Error deleting {error['Key']}: {error['Code']} - {error['Message']}")
        
        return deleted_count
    except ClientError as e:
        print(f"Error occurred: {e}")
        return 0

def list_and_delete_objects(bucket_name, delete_existing=False):
    """
    List and delete objects (including versions and delete markers) from the S3 bucket.
    
    Args:
    bucket_name (str): Name of the S3 bucket.
    delete_existing (bool): If True, delete all versions including the latest. If False, keep the latest version.
    
    Returns:
    int: Total number of deleted objects.
    """
    paginator = s3_client.get_paginator('list_object_versions')
    total_deleted = 0
    objects_to_delete = []

    for page in paginator.paginate(Bucket=bucket_name):
        # Process object versions
        for version in page.get('Versions', []):
            if delete_existing or not version['IsLatest']:
                objects_to_delete.append({
                    'Key': version['Key'],
                    'VersionId': version['VersionId']
                })
        
        # Process delete markers
        for marker in page.get('DeleteMarkers', []):
            objects_to_delete.append({
                'Key': marker['Key'],
                'VersionId': marker['VersionId']
            })
        
        # Delete objects in batches
        if len(objects_to_delete) >= 1000:
            total_deleted += delete_objects(bucket_name, objects_to_delete[:1000])
            objects_to_delete = objects_to_delete[1000:]
            print(f"Total deleted so far: {total_deleted}")

    # Delete any remaining objects
    if objects_to_delete:
        total_deleted += delete_objects(bucket_name, objects_to_delete)

    return total_deleted

def main():
    """
    Main function to run the S3 object deletion script.
    """
    parser = argparse.ArgumentParser(description="Delete objects from an S3 bucket.")
    parser.add_argument("--delete_existing", type=bool, default=os.getenv("DELETE_EXISTING", "False") == "True", 
                        help="Delete all versions including the latest.")
    parser.add_argument("--bucket_name", type=str, default=os.getenv("BUCKET_NAME"), 
                        help="Name of the S3 bucket.")
    args = parser.parse_args()

    if not args.bucket_name:
        print("Error: Bucket name must be provided either as an environment variable or argument.")
        return

    try:
        total_deleted = list_and_delete_objects(args.bucket_name, args.delete_existing)
        print(f"Total objects deleted: {total_deleted}")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
