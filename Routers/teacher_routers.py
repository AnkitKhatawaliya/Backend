from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from DataBase.DB_teacher import DB_validate_teacher, DB_get_Class_records, DB_Mark_Attendance, DB_get_teacher_info
from DataBase.DB_teacher import DB_give_Marks, DB_add_Notice
from DataBase.DB_teacher import DB_Update_Homework, DB_get_Notices, DB_get_Attendance, DB_get_Marks
from DataBase.DB_teacher import DB_get_Homework, DB_get_teacher_schedule
from Models.Teacher_schemas import Homework_Model, Notices_Model
from Security.Hash import Convert_to_hash
from Security.jwt_methods import create_jwt_token_int

router = APIRouter()


@router.get('/validate_teacher/{ID}/{password}', status_code=status.HTTP_202_ACCEPTED)
def Validate_Teacher(ID: int, password: str):
    password = Convert_to_hash(password)
    data = DB_validate_teacher(ID, password)
    if data is True:
        token = create_jwt_token_int(ID, "Teacher")
        return {"Token": token}
    elif data is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=["Invalid credentials"])
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["Some Error"])


@router.get('/homepage_info/{ID}', status_code=status.HTTP_202_ACCEPTED)
def HomePageInfo(ID: int):
    Info = DB_get_teacher_info(ID)
    if Info is not None:
        return Info
    elif Info is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=["Not Exists"])
    elif Info is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["Some Error"])





@router.get("/get_class_records/{Standard}/{Section}")
def Get_Class_Records(Standard: int, Section: str):
    Data = DB_get_Class_records(Standard, Section)
    if Data is not None:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])


@router.post("/mark_attendance/{Standard}/{Section}")
def Mark_Attendance(Standard: int, Section: str, Attendance: dict):
    if DB_Mark_Attendance(Standard, Section, Attendance):
        return {"Attendance": "Marked"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])


@router.post("/Give_marks/{Standard}/{Section}/{Subject}/{Max_marks}")
def Give_marks(Standard: int, Section: str, Subject: str, Max_marks: int, Marks: dict):
    if DB_give_Marks(Standard, Section, Subject, Max_marks, Marks):
        return {"Attendance": "Marked"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])


@router.post('/Add_Homework')
def Update_Homework(Homework: Homework_Model):
    if DB_Update_Homework(Homework):
        return {"Homework": "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])


@router.get('/get_attendance/{Standard}/{Section}')
def Get_attendance(Standard: int, Section: str):
    Data = DB_get_Attendance(Standard, Section)
    if Data is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])
    else:
        return Data


@router.get('/get_marks/{Standard}/{Section}/{Subject}')
def Get_marks(Standard: int, Section: str, Subject: str):
    Data = DB_get_Marks(Standard, Section, Subject)
    if Data is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])
    else:
        return Data


@router.get("/fetch_homework/{Standard}/{Section}/{Subject}")
def Get_homework(Standard: int, Section: str, Subject: str):
    Data = DB_get_Homework(Standard, Section, Subject)
    if Data is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])
    else:
        return Data


@router.get("/Fetch_Schedule/{ID}")
def Get_Schedule(ID: int):
    Data = DB_get_teacher_schedule(ID)
    if Data is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])
    else:
        return Data


@router.post('/notice')
def add_notice(Notice: Notices_Model):
    if DB_add_Notice(Notice):
        return {'Notice': "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/notices')
def get_notices():
    Data = DB_get_Notices()
    if Data:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
