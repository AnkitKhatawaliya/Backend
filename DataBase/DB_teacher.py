from datetime import datetime

from DataBase.DB_conn import fetch_from_database, Fetch_all_from_database, Execute_on_DB, Insert_on_DB, \
    Fetch_par_from_database
from Models.Teacher_schemas import Homework_Model


def DB_validate_teacher(ID: int, password: str):
    print(ID, password)
    Query = "SELECT * FROM Teacher_records WHERE ID = %s"
    Value = ID
    result = fetch_from_database(Query, Value)
    if result[password] == password:
        return True
    else:
        return False


def DB_get_Class_records(Standard: int, Section: str):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context = 'Name'"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_Mark_Attendance(Standard: int, Section: str, Attendance: dict):
    ClassName = f"class{Standard}{Section}"
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Combined query for inserting date, context, and attendance
    Query_combined = f"""INSERT INTO {ClassName} (Date, Context,"""

    for i, j in Attendance.items():
        Query_combined += f" Roll_NO_{i},"

    # Remove the trailing comma and add the VALUES part
    Query_combined = Query_combined.rstrip(',') + f") VALUES ('{current_date}', 'Attendance',"

    values_str = ",".join([f" {j}" for i, j in Attendance.items()])
    Query_combined += f"{values_str});"

    try:
        Execute_on_DB(Query_combined)
    except Exception as e:
        print(e)
        return False
    return True


def DB_give_Marks(Standard: int, Section: str, Subject: str, Max_marks: int, Marks: dict):
    ClassName = f"class{Standard}{Section}"
    current_date = datetime.now().strftime('%Y-%m-%d')
    Context = f"{Subject}_{Max_marks}"
    Query_combined = f"""INSERT INTO {ClassName} (Date, Context,"""

    for i, j in Marks.items():
        Query_combined += f" Roll_NO_{i},"

    # Remove the trailing comma and add the VALUES part
    Query_combined = Query_combined.rstrip(',') + f") VALUES ('{current_date}', '{Context}',"

    values_str = ",".join([f" {j}" for i, j in Marks.items()])
    Query_combined += f"{values_str});"

    try:
        Execute_on_DB(Query_combined)
    except Exception as e:
        print(e)
        return False
    return True


def DB_Update_Homework(Homework: Homework_Model):
    Query = f"""
    UPDATE HomeWork_Table
    SET {Homework.Day} = %s
    WHERE Subject = %s
    AND Standard = %s
    AND Section = %s    
    """
    Values = (
        Homework.Homework, Homework.Subject, Homework.Standard, Homework.Section
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True


def DB_get_Attendance(Standard, Section):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context = 'Attendance'"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_get_Marks(Standard, Section, Subject: str):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context LIKE %s"
    Value = f"{Subject}_%"
    try:
        Data = Fetch_par_from_database(Query, Value)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_get_Homework(Standard, Section, Subject: str):
    Query = f"SELECT * FROM HomeWork_Table WHERE Standard = %s AND Section = %s AND Subject = %s"
    Values = (Standard, Section, Subject,)
    try:
        Data = Fetch_par_from_database(Query, Values)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_get_teacher_schedule(teacher_id: int):
    query = (
        "SELECT Standard, Section FROM Time_Table WHERE "
        "Lect_1 = %s OR Lect_2 = %s OR Lect_3 = %s OR "
        "Lect_4 = %s OR Lect_5 = %s OR Lec_6 = %s OR "
        "Lect_7 = %s OR Lec_8 = %s"
    )
    values = (teacher_id, teacher_id, teacher_id, teacher_id, teacher_id, teacher_id, teacher_id, teacher_id)
    try:
        data = Fetch_par_from_database(query, values)
    except Exception as e:
        print(e)
        return False
    return data


def DB_get_Notices():
    Table_name = f"Notices_Table"
    Query = f"SELECT * FROM {Table_name} ORDER BY Sr_no"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data
