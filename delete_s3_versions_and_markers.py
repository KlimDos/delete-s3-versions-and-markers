import boto3

BUCKET_NAME = 'YOUR_BUCKET_NAME'

s3_client = boto3.client('s3')

def delete_objects(delete_list):
    if delete_list:
        print(f"Deleting {len(delete_list)} objects...")
        s3_client.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={
                'Objects': delete_list
            }
        )

def main():
    paginator = s3_client.get_paginator('list_objects_v2')  # Use 'list_objects_v2' instead of 'list_object_versions'
    pages = paginator.paginate(Bucket=BUCKET_NAME)

    delete_list = []
    total_deleted = 0

    for page in pages:
        if 'Contents' in page:  # Check for existing objects
            for obj in page['Contents']:
                delete_list.append({
                    'Key': obj['Key'],
                })
                if len(delete_list) == 1000:
                    delete_objects(delete_list)
                    total_deleted += len(delete_list)
                    print(f"Total deleted so far: {total_deleted}")
                    delete_list = []

        if 'Versions' in page:
            for version in page['Versions']:
                delete_list.append({
                    'Key': version['Key'],
                    'VersionId': version['VersionId']
                })
                if len(delete_list) == 1000:
                    delete_objects(delete_list)
                    total_deleted += len(delete_list)
                    print(f"Total deleted so far: {total_deleted}")
                    delete_list = []

        if 'DeleteMarkers' in page:
            for marker in page['DeleteMarkers']:
                delete_list.append({
                    'Key': marker['Key'],
                    'VersionId': marker['VersionId']
                })
                if len(delete_list) == 1000:
                    delete_objects(delete_list)
                    total_deleted += len(delete_list)
                    print(f"Total deleted so far: {total_deleted}")
                    delete_list = []

    delete_objects(delete_list)
    total_deleted += len(delete_list)
    print(f"Total deleted: {total_deleted}")

if __name__ == "__main__":
    main()
