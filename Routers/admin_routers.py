import tempfile
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from DataBase.DB_admin import DB_Add_Teacher, DB_delete_Teacher, DB_Get_Teachers, DB_add_Time_Table
from DataBase.DB_admin import DB_Create_Class_Table, DB_add_a_student, DB_get_Class_records
from DataBase.DB_admin import DB_Create_HW_Table, DB_Config_HW_Table, DB_delete_a_student
from DataBase.DB_admin import DB_delete_time_table, DB_get_time_tale, DB_add_Notice, DB_delete_Notice, DB_get_Notices
from Models.Admin_schemas import AdminLogin, Class_Table, StudentModel, TeacherModel, TimeTableModel, Notices_Model
from Security.AWS_methods import Upload_to_Cloud, Download_from_cloud
from Security.jwt_methods import create_jwt_token

router = APIRouter()


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def admin_login(User: AdminLogin):
    if User.ID == "pankaj" and User.Password == "PASSWORD":
        token = create_jwt_token(User.ID, "Admin")
        return {"Login": "Success", "Token": token}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=["error"])


@router.post('/CST')
def Create_Student_Table(Class: Class_Table):
    if DB_Create_Class_Table(Class.Standard, Class.Section):
        return {"Class table": "Created"}
    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=["error"])


@router.post('/add_student')
def Add_Student_in_Table(Student: StudentModel):
    if DB_add_a_student(Student):
        return {f"Student {Student.Name}": "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=["error"])


@router.post('/add_student_image/{ADM_NO}')
def Add_Student_Image(ADM_NO: int, student_image: UploadFile = File(...)):
    file_path = f"imagefile"
    Name = f"{ADM_NO}.jpg"
    with open(file_path, "wb") as f:
        f.write(student_image.file.read())
    Upload_to_Cloud(Name, file_path, "Student")
    return {"Photo": "Uploaded"}


@router.get('/student_image/{ADM_NO}')
def get_Student_Image(ADM_NO: int):
    Name = f"{ADM_NO}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    try:
        Download_from_cloud(Name, File_path.name, "Student")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return FileResponse(File_path.name, media_type='image/jpeg')


@router.get('/get_students/{Standard}/{Section}')
def Get_Student(Standard: int, Section: str):
    Data = DB_get_Class_records(Standard, Section)
    if not Data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=["error"])
    else:
        return Data


@router.delete('/delete_student/{Standard}/{Section}/{Roll_NO}')
def Delete_Student(Standard: int, Section: str, Roll_NO: int):
    if DB_delete_a_student(Standard, Section, Roll_NO):
        return {'Deletion': "Complete"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


# ----------------------------------------------------------------
# Routes for Teachers

@router.post('/add_teacher')
def Add_Teacher(Teacher: TeacherModel):
    if DB_Add_Teacher(Teacher):
        return {'Teacher': "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/teachers')
def Get_Teachers():
    Data = DB_Get_Teachers()
    if Data:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.delete('/delete_teacher/{ID}')
def Delete_teacher(ID: int):
    if DB_delete_Teacher(ID):
        return {'Teacher': "Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


# ----------------------------------------------------------------
# Routes for time table

@router.post('/time_table')
def add_time_table(TimeTable: TimeTableModel):
    if DB_add_Time_Table(TimeTable):
        return {'Schedule': "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/time_table/{Standard}/{Section}/{Weekday}')
def delete_time_table(Standard: int, Section: str, Weekday: str):
    if DB_delete_time_table(Standard, Section, Weekday):
        return {'Schedule': "Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/time_table/{Standard}/{Section}')
def get_time_table(Standard: int, Section: str):
    Data = DB_get_time_tale(Standard, Section)
    if Data:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


# ----------------------------------------------------------------
# Calendar Routes

@router.post('/notice')
def add_notice(Notice: Notices_Model):
    if DB_add_Notice(Notice):
        return {'Notice': "Added"}
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.delete('/notice/{Sr_no}')
def delete_a_notice(Sr_no: int):
    if DB_delete_Notice(Sr_no):
        return {'Schedule': "Deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/notices')
def get_notices():
    Data = DB_get_Notices()
    if Data:
        return Data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


# ----------------------------------------------------------------
# Homework Routes


@router.get('/Create_HW_Table')
def Create_HW_Table():
    if DB_Create_HW_Table():
        return {'Table': "Created"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/Config_HW_Table/{Standard}/{Section}/{Subject}")
def add_class_homework(Standard: str, Section: str, Subject: str):
    if DB_Config_HW_Table(Standard, Section, Subject):
        return {'Table': "Created"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
