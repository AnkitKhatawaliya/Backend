from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile
import boto3
from Security.JWT import get_current_user

router = APIRouter()

s3 = boto3.client(
    's3',
    region_name='ap-south-1',
    aws_access_key_id='AKIAQXTKJT7HIWODQMVM',
    aws_secret_access_key='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'
)

Bucket_name = "images-school"


def Upload_to_Cloud(Name: str, File_path: str):
    s3.upload_file(File_path, Bucket_name, Name)


def Download_from_cloud(Image_name: str, File_path: str):
    try:
        with open(File_path, 'wb') as f:
            s3.download_fileobj(Bucket_name, Image_name, f)
    except Exception as e:
        raise e


@router.get("/images/{Name}")
def SendImage(Name: str, current_user: str = Depends(get_current_user)):
    File_path = tempfile.NamedTemporaryFile(delete=False)
    Download_from_cloud(Name, File_path.name)
    return FileResponse(File_path.name, media_type='image/jpeg')


@router.post("/images/{Name}")
def Recieve_Image(Name: str, current_user: str = Depends(get_current_user), image: UploadFile = File(...)):
    file_path = f"{Name}"
    try:
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        Upload_to_Cloud(Name, file_path)
        os.remove(file_path)
        return {'Image': "Upload Successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=403)
