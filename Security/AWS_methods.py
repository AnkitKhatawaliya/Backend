import boto3


s3 = boto3.client(
    's3',
    region_name='ap-south-1',
    aws_access_key_id='AKIAQXTKJT7HIWODQMVM',
    aws_secret_access_key='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'
)

Student_Bucket = "images-school"
General_Bucket = "side-files"


def Upload_to_Cloud(Name: str, File_path: str, Where: str):
    if Where == "Student":
        s3.upload_file(File_path, Student_Bucket, Name)
    elif Where == "General":
        s3.upload_file(File_path, General_Bucket, Name)


def Download_from_cloud(Image_name: str, File_path: str, Where: str):
    if Where == "Student":
        try:
            with open(File_path, 'wb') as f:
                s3.download_fileobj(Student_Bucket, Image_name, f)
        except Exception as e:
            raise e
    elif Where == "General":
        try:
            with open(File_path, 'wb') as f:
                s3.download_fileobj(General_Bucket, Image_name, f)
        except Exception as e:
            raise e
