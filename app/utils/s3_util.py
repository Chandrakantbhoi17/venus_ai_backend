import boto3
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings

def upload_file_to_s3(file: UploadFile, query_id:int) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION)

    file_ext = file.filename.split(".")[-1]
    key = f"{query_id}/{uuid4()}.{file_ext}"

    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{key}"
