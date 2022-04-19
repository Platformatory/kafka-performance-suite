#!/usr/bin/env python3
import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def env_check(key):
  if key not in os.environ:
    print(f"{key} not found. Exiting...")
    sys.exit(1)
  else:
    return os.environ[key]
    
ACCESS_KEY = env_check('ACCESS_KEY')
SECRET_KEY = env_check('SECRET_KEY')

test_prefix = env_check('TEST_PREFIX')
bucket = env_check('BUCKET')

filename = sys.argv[1]

if not filename:
  print('filename parameter not given. Exiting...')
  sys.exit(1)
        
uploaded = upload_to_aws(filename, bucket, f"{test_prefix}/{filename}")
