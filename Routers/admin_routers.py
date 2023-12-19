import tempfile
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from DataBase.DB_admin import DB_Create_Class_Table, DB_add_a_student, DB_get_Class_records, DB_delete_a_student
from Models.Admin_schemas import AdminLogin, Class_Table, StudentModel
from Security.AWS_methods import Upload_to_Cloud, Download_from_cloud
from Security.JWT import create_jwt_token

router = APIRouter()


@router.post('/login')
def admin_login(User: AdminLogin):
    if User.ID == "pankaj" and User.Password == "PASSWORD":
        token = create_jwt_token(User.ID)
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
def Add_Student_Image(ADM_NO: int, student_image:UploadFile = File(...)):
    file_path = f"random"
    Name = f"{ADM_NO}.jpg"
    with open(file_path, "wb") as f:
        f.write(student_image.file.read())
    Upload_to_Cloud(Name, file_path)
    return {"Photo": "Uploaded"}


@router.get('/student_image/{ADM_NO}')
def get_Student_Image(ADM_NO: int):
    Name = f"{ADM_NO}.jpg"
    File_path = tempfile.NamedTemporaryFile(delete=False)
    Download_from_cloud(Name, File_path.name)
    return FileResponse(File_path.name, media_type='image/jpeg')


@router.get('/get_students/{Standard}/{Section}')
def Get_Student(Standard: int, Section: str):
    Data = DB_get_Class_records(Standard, Section)
    if not Data:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=["error"])
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
