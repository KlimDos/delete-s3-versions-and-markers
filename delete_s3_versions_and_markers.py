import boto3

BUCKET_NAME = 'insert s3 bucket name'

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
    paginator = s3_client.get_paginator('list_object_versions')
    pages = paginator.paginate(Bucket=BUCKET_NAME)

    delete_list = []
    total_deleted = 0

    for page in pages:
        if 'Versions' in page:
            for version in page['Versions']:
                if not version['IsLatest']:
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
