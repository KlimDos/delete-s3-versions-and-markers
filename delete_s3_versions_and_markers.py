import boto3
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = 'YOUR_BUCKET_NAME'
BATCH_SIZE = 1000  # Maximum number of objects to delete in a single API call

# Initialize S3 client
s3_client = boto3.client('s3')

def delete_objects(objects_to_delete):
    """
    Delete a batch of objects from the S3 bucket.
    
    Args:
    objects_to_delete (list): List of dictionaries containing 'Key' and 'VersionId' of objects to delete.
    
    Returns:
    int: Number of successfully deleted objects.
    """
    if not objects_to_delete:
        return 0

    try:
        response = s3_client.delete_objects(
            Bucket=BUCKET_NAME,
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

def list_and_delete_objects(delete_existing=False):
    """
    List and delete objects (including versions and delete markers) from the S3 bucket.
    
    Args:
    delete_existing (bool): If True, delete all versions including the latest. If False, keep the latest version.
    
    Returns:
    int: Total number of deleted objects.
    """
    paginator = s3_client.get_paginator('list_object_versions')
    total_deleted = 0
    objects_to_delete = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):
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
        if len(objects_to_delete) >= BATCH_SIZE:
            total_deleted += delete_objects(objects_to_delete[:BATCH_SIZE])
            objects_to_delete = objects_to_delete[BATCH_SIZE:]
            print(f"Total deleted so far: {total_deleted}")

    # Delete any remaining objects
    if objects_to_delete:
        total_deleted += delete_objects(objects_to_delete)

    return total_deleted

def main():
    """
    Main function to run the S3 object deletion script.
    """
    try:
        delete_existing = input("Do you want to delete existing objects? (y/n): ").lower() == 'y'
        total_deleted = list_and_delete_objects(delete_existing)
        print(f"Total objects deleted: {total_deleted}")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
