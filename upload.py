import logging
import os

import boto3
import psycopg2
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None, content_type="audio/mpeg"):
    """Upload a file to an S3 bucket with specified content type for browser streaming.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :param content_type: The content type of the file (e.g., "audio/mpeg", "video/mp4"). Defaults to "audio/mpeg"
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file with ContentType metadata
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(
            file_name,
            bucket,
            object_name,
            ExtraArgs={"ContentType": content_type},
        )
        print(response)  # added for debugging
    except ClientError as e:
        logging.error(e)
        return False
    return True


def add_to_db(url):
    print(f"Adding {url} to the database")
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute("INSERT INTO summaries (url) VALUES (%s)", (url,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"{url} added to the database.")


if __name__ == "__main__":
    file_name = "reddit_news_summary.mp3"
    bucket_name = "hackathon"
    object_name = file_name

    if upload_file(file_name, bucket_name, object_name):
        endpoint_url = os.environ.get("AWS_ENDPOINT_URL_S3")
        file_url = f"{endpoint_url}/{bucket_name}/{object_name}"
        print(f"File URL: {file_url}")
    else:
        print("File upload failed.")

    url = "https://example.com"
    add_to_db(url)
    print("URL added to the database.")
