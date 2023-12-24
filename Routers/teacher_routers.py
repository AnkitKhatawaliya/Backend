from fastapi import APIRouter, status, HTTPException
from DataBase.DB_teacher import DB_validate_teacher, DB_get_Class_records, DB_Mark_Attendance, DB_give_Marks, \
    DB_Update_Homework, DB_get_Notices, DB_get_Attendance, DB_get_Marks, DB_get_Homework, DB_get_teacher_schedule
from Models.Teacher_schemas import Homework_Model
from Security.Hash import Convert_to_hash
from Security.JWT import create_jwt_token_int

router = APIRouter()


@router.get('/validate_teacher/{ID}/{password}', status_code=status.HTTP_202_ACCEPTED)
def Validate_Teacher(ID: int, password: str):
    password = Convert_to_hash(password)
    if DB_validate_teacher(ID, password):
        token = create_jwt_token_int(ID, "Teacher")
        return {"Password": "Verified", "Token": token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=["error"])


@router.get("/get_class _records/{Standard}/{Section}")
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


@router.get('/notices')
def get_notices():
    Data = DB_get_Notices()
    if Data:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
