import tempfile
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from Security.AWS_methods import Upload_to_Cloud, Download_from_cloud

router = APIRouter()


@router.post('/Teacher_image/{ID}')
def Add_Teacher_Image(ID: int, student_image: UploadFile = File(...)):
    file_path = f"imagefile"
    Name = f"{ID}.jpg"
    with open(file_path, "wb") as f:
        f.write(student_image.file.read())
    Upload_to_Cloud(Name, file_path, "General")
    return {"Photo": "Uploaded"}


@router.get('/Teacher_image/{ID}')
def get_Student_Image(ID: int):
    Name = f"{ID}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    try:
        Download_from_cloud(Name, File_path.name, "General")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return FileResponse(File_path.name, media_type='image/jpeg')


@router.post('/Basic_image/{Name}')
def Add_Teacher_Image(Name: str, student_image: UploadFile = File(...)):
    file_path = f"imagefile"
    Name = f"{Name}.jpg"
    with open(file_path, "wb") as f:
        f.write(student_image.file.read())
    Upload_to_Cloud(Name, file_path, "General")
    return {"Photo": "Uploaded"}


@router.get('/Basic_image/{Name}')
def get_Student_Image(Name: str):
    Name = f"{Name}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    try:
        Download_from_cloud(Name, File_path.name, "General")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return FileResponse(File_path.name, media_type='image/jpeg')
