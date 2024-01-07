from datetime import datetime
from DataBase.DB_conn import Fetch_all_from_database, Execute_on_DB, Insert_on_DB
from DataBase.DB_conn import Fetch_par_from_database
from Models.Teacher_schemas import Homework_Model, Notices_Model


def DB_validate_teacher(ID: int, password: str):
    Query = f"SELECT * FROM Teacher_Table WHERE ID = {ID}"
    result = Fetch_all_from_database(Query)
    if result[0][2] == password:
        return True
    elif result[0][2] != password:
        return False
    else:
        return None


def DB_get_teacher_info(ID: int):
    Query = f"SELECT * FROM Teacher_Table WHERE ID ={ID}"
    try:
        result = Fetch_all_from_database(Query)
        if not result:
            return None
        else:
            return result
    except:
        return False


def DB_get_Class_records(Standard: int, Section: str):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context = 'Name' OR Context = 'Roll_No'"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_Mark_Attendance(Standard: int, Section: str, Attendance: dict):
    ClassName = f"class{Standard}{Section}"
    current_date = datetime.now().strftime('%Y-%m-%d')

    Query_combined = f"""INSERT INTO {ClassName} (Date, Context,"""

    for i, j in Attendance.items():
        Query_combined += f" Roll_NO_{i},"

    Query_combined = Query_combined.rstrip(',') + f") VALUES ('{current_date}', 'Attendance',"

    values_str = ",".join([f" '{j}'" for i, j in Attendance.items()])
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

    Query_combined = Query_combined.rstrip(',') + f") VALUES ('{current_date}', '{Context}',"

    values_str = ",".join([f" '{j}'" for i, j in Marks.items()])
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
        Homework.Homework, Homework.Subject, f'{Homework.Standard}', Homework.Section
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True


def DB_get_Attendance(Standard, Section):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context = 'Attendance' OR Context = 'Name'"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_get_Marks(Standard, Section, Subject: str):
    ClassName = f"class{Standard}{Section}"
    Query = f"SELECT * FROM {ClassName} WHERE Context LIKE %s OR Context = 'Name'"
    Value = (f"{Subject}_%",)
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


def DB_get_teacher_schedule(teacher_id: str):
    query = (
        "SELECT Standard, Section, weekday FROM Time_Table WHERE "
        "Lect_1 = %s OR Lect_2 = %s OR Lect_3 = %s OR "
        "Lect_4 = %s OR Lect_5 = %s OR Lect_6 = %s OR "
        "Lect_7 = %s OR Lect_8 = %s"
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


def DB_add_Notice(Notice: Notices_Model):
    current_date = datetime.now().strftime('%Y-%m-%d')
    Receiver = "class" + f"{Notice.Standard}" + f"{Notice.Section}"
    Query = """
    INSERT INTO Notices_Table (Title, Heading, Description, Send_DATE, For_Date, Receiver)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    Values = (
        Notice.Title,
        Notice.Heading,
        Notice.Description,
        current_date,
        Notice.for_date,
        Receiver
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True
