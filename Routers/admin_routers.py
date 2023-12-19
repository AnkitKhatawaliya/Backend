from fastapi import APIRouter, UploadFile, File, HTTPException , status
from DataBase.DB_admin import DB_Create_Class_Table, DB_add_a_student, DB_get_Class_records
from Models.Admin_schemas import AdminLogin, Class_Table, StudentModel
from Security.AWS_methods import Upload_to_Cloud
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
def Add_Student_Image(ADM_NO: int, student_image: UploadFile = File(...)):
    file_path = f"random"
    Name = f"{ADM_NO}.jpg"
    with open(file_path, "wb") as f:
        f.write(student_image.file.read())
    Upload_to_Cloud(Name, file_path)
    return {"Photo": "Uploaded"}


@router.post('/get_students')
def Get_Student(Class: Class_Table):
    Data = DB_get_Class_records(Class)
    if not Data:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=["error"])
    else:
        return Data
