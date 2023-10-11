# AWS S3 Versioned Cleanup Script

This Python script is designed to delete 'old object versions' and 'delete markers' from an AWS S3 bucket with versioning enabled. 

## Prerequisites:

- Python (tested on version 3.6+)
- `boto3` library: The AWS SDK for Python
- Properly configured AWS credentials, either through the AWS CLI or environment variables

## Installation:

1. Clone the repository or download the script
2. Install `boto3`: `pip install boto3`
3. Ensure your AWS credentials are set up. This can be done using the AWS CLI: `aws configure`

Follow the prompts to input your AWS access key, secret key, default region, and default output format (e.g., `json`).

## Usage:

1. Open the script in a text editor and replace `'YOUR_BUCKET_NAME'` with the name of your bucket.
2. Run the script: python  


## Important Notes:

- **Backup First**: Always backup critical data before running scripts that perform deletion operations.

- **Test Before Use**: Consider testing on a subset of your data or using a backup before running the script on large or important datasets.

- **AWS Costs**: Depending on the number of versions and delete markers you have, and how often you run the script, you might incur charges for the DELETE requests and for retrieving versioning information.

## Contributions:

Feel free to fork this repository, make improvements, and submit pull requests. Feedback and suggestions are welcome!

