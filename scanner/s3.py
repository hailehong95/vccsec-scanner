#!/usr/bin/env python

import os
import json
import boto3
import base64
import codecs
import datetime
import requests

from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from scanner.setting import TEST_DIR, BASE_URL
from scanner.setting import SNIPPET_URL as snippet_url


# Ref: https://stackoverflow.com/a/35870294
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def pretty_print(data):
    print(json.dumps(data, sort_keys=False, indent=4, default=datetime_handler))


def write_json_file(json_data, file_name):
    try:
        with open(os.path.join(TEST_DIR, file_name), 'w') as fs:
            json.dump(json_data, fs, sort_keys=False, indent=4, default=datetime_handler)
    except Exception as err:
        print(err)


def bzc_load_config():
    try:
        res = requests.get(snippet_url)
        return json.loads(base64.b64decode(codecs.decode(res.text, 'rot_13')).decode())
    except Exception as err:
        print(err)


def bzc_sts_client_init():
    try:
        config = bzc_load_config()
        sts_client = boto3.client('sts', endpoint_url=BASE_URL, aws_access_key_id=config['ACCESS_KEY'],
                                  aws_secret_access_key=config['SECRET_KEY'], region_name='')
        return sts_client
    except Exception as err:
        print(err)
    return None


def bzc_s3_client_init():
    try:
        config = bzc_load_config()
        s3_client = boto3.client('s3', endpoint_url=BASE_URL, aws_access_key_id=config['ACCESS_KEY'],
                                 aws_secret_access_key=config['SECRET_KEY'])
        return s3_client
    except Exception as err:
        print(err)
    return None


def bzc_s3_resource_init():
    try:
        config = bzc_load_config()
        s3_resource = boto3.resource('s3', endpoint_url=BASE_URL, aws_access_key_id=config['ACCESS_KEY'],
                                     aws_secret_access_key=config['SECRET_KEY'])
        return s3_resource
    except Exception as err:
        print(err)
    return None


# # Status: An error occurred (Unknown) when calling the GetSessionToken operation: Unknown
def bzc_get_session_token():
    try:
        time_expired = 12 * 60 * 60
        sts_client = bzc_sts_client_init()
        temp_token = sts_client.get_session_token(DurationSeconds=time_expired)
        return temp_token
    except Exception as err:
        print(err)
    return None


# Get a bucket access control list
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-access-permissions.html
def bzc_access_permissions(bucket):
    try:
        # Retrieve a bucket's ACL
        s3_client = bzc_s3_client_init()
        result = s3_client.get_bucket_acl(Bucket=bucket)
        return result
    except Exception as err:
        print(err)
    return None


# Create an Amazon S3 bucket
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
def bzc_create_bucket(bucket_name, region=None):
    """
    Create an S3 bucket in a specified region
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    try:
        s3_client = bzc_s3_client_init()
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as err:
        print(err)
        return False
    return True


# List existing buckets
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
def bzc_list_bucket():
    try:
        s3_client = bzc_s3_client_init()
        response = s3_client.list_buckets()
        return response
    except ClientError as err:
        print(err)
    return None


def bzc_list_file(bucket):
    try:
        s3_client = bzc_s3_client_init()
        response = s3_client.list_objects(Bucket=bucket)
        return response
    except ClientError as err:
        print(err)
    return None


# Upload a file to an S3 bucket
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def bzc_upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file
    s3_client = bzc_s3_client_init()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(e)
        return False
    return True


# Multipart upload - Upload các tệp tin có kích thước lớn.
# Ref: https://support.bizflycloud.vn/api/simple-storage/?python--boto3#multipart-upload
def bzc_multipart_upload(file_name, bucket, object_name=None):
    """
    Multipart upload. Size của 1 part tối thiểu là 5MB.
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = bzc_s3_client_init()
    try:
        config = TransferConfig(
            multipart_threshold=5 * 1024 ** 3,  # 5GB
            max_concurrency=10,
            num_download_attempts=10
        )
        response = s3_client.upload_file(file_name, bucket, object_name, Config=config)
    except ClientError as e:
        print(e)
        return False
    return True


def bzc_upload_fileobj(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file
    s3_client = bzc_s3_client_init()
    try:
        with open(file_name, 'rb') as fs:
            s3_client.upload_fileobj(fs, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True


# Downloading files
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
def bzc_download_file(bucket, object_name, file_name=None):
    """
    Download a file from an S3 bucket
    :param bucket: Bucket to download
    :param object_name: S3 object name to download
    :param file_name: File to saved
    :return: True if file was downloaded, else False
    """
    # If file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name
    # Download the file
    s3_client = bzc_s3_client_init()
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except ClientError as e:
        print(e)
        return False
    return True


# Retrieve a bucket policy
# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-bucket-policies.html
# Status: The bucket policy does not exist
def bzc_get_bucket_policy(bucket):
    try:
        s3_client = bzc_s3_client_init()
        result = s3_client.get_bucket_policy(Bucket=bucket)
        return result
    except ClientError as e:
        print(e)
    return None
