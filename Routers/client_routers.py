import tempfile
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from DataBase.DB_client import DB_Validate_Student, DB_Validate_Parent, DB_Basic_Info
from DataBase.DB_client import DB_Fetch_TimeTable
from DataBase.DB_client import DB_Fetch_Notices, DB_Get_Homework
from Models.Client_Schemas import Validation_Model
from Security.AWS_methods import Download_from_cloud
from Security.jwt_methods import create_jwt_token_int

router = APIRouter()


@router.post('/validate_Client')
def validate_client(Data: Validation_Model):
    if Data.Role == "Parent":
        Result = DB_Validate_Parent(Data)
        if Result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if Result is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if Result is True:
            Token = create_jwt_token_int(Data.Roll_NO, "Client")
            return {"Token": Token}

    elif Data.Role == "Student":
        Result = DB_Validate_Student(Data)
        if Result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if Result is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if Result is True:
            Token = create_jwt_token_int(Data.Roll_NO, "Client")
            return {"Login": "Successful", "Token": Token}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/Image/{ADM_NO}')
def get_Student_Image(ADM_NO: int):
    Name = f"{ADM_NO}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    try:
        Download_from_cloud(Name, File_path.name, "Student")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return FileResponse(File_path.name, media_type='image/jpeg')


@router.get('/Home_page_info/{Standard}/{Section}/{Roll_NO}')
def Get_hp_info(Standard: int, Section: str, Roll_NO: int):
    Data = DB_Basic_Info(Standard, Section, Roll_NO)

    if Data is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    elif not Data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        return Data


@router.get('/Home_Work/{Standard}/{Section}')
def Get_Homework(Standard: str, Section: str):
    Homework = DB_Get_Homework(Standard, Section)
    if Homework is not None:
        return Homework
    elif Homework is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/Notices/{Standard}/{Section}')
def Get_Notices(Standard: str, Section: str):
    Notices = DB_Fetch_Notices(Standard, Section)
    if Notices is not None:
        return Notices
    elif Notices is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/Time_table/{Standard}/{Section}')
def Get_Time_table(Standard: int, Section: str):
    Time_table = DB_Fetch_TimeTable(Standard, Section)
    if Time_table is not None:
        return Time_table
    elif Time_table is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
