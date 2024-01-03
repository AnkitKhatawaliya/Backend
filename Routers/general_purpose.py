import tempfile
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from Security.AWS_methods import Download_from_cloud

router = APIRouter()


@router.get('/Basic_image/{Name}')
def Get_Image(Name: str):
    Name = f"{Name}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    try:
        Download_from_cloud(Name, File_path.name, "General")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return FileResponse(File_path.name, media_type='image/jpeg')
