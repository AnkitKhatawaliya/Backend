from datetime import datetime
from Models.Admin_schemas import StudentModel, Class_Table

from DataBase.connection import Execute_on_DB, Fetch_all_from_database


def DB_Create_Class_Table(Standard: int, Section: str):
    ClassName = "class" + f"{Standard}" + Section
    Query = f"""CREATE TABLE IF NOT EXISTS {ClassName} (
        Date DATE,
        Context VARCHAR(50),
        PRIMARY KEY (Date, Context)
    );
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    InsertQuery = f"""INSERT INTO {ClassName} (Date, Context)
    VALUES 
        ('{current_date}', 'Adm_NO'),
        ('{current_date}', 'Name'),
        ('{current_date}', 'D.O.B'),
        ('{current_date}', 'Gender'),
        ('{current_date}', 'Parent_Name'),
        ('{current_date}', 'Parent_NO'),
        ('{current_date}', 'Password'),
        ('{current_date}', 'Parent_PSD');
    """
    try:
        Execute_on_DB(Query)
        Execute_on_DB(InsertQuery)
    except Exception as e:
        print(e)
        return False
    return True


def DB_add_a_student(Student: StudentModel):
    ClassName = f"class{Student.Standard}{Student.Section}"
    ColumnsName = f"Roll_NO_{Student.Roll_NO}"
    add_column_query = f"ALTER TABLE {ClassName} ADD COLUMN IF NOT EXISTS {ColumnsName} TEXT"
    Insert_Query = (f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Adm_NO}' WHERE Context = 'Adm_NO';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Name}' WHERE Context = 'Name';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.DOB}' WHERE Context = 'D.O.B';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Gender}' WHERE Context = 'Gender';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Parent_Name}' WHERE Context = 'Parent_Name';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Parent_NO}' WHERE Context = 'Parent_NO';"
                    f"UPDATE {ClassName} SET {ColumnsName} = '{Student.Password}' WHERE Context = 'Password';"
                    f" UPDATE {ClassName} SET {ColumnsName} = '{Student.Parent_PSD}' WHERE Context = 'Parent_PSD';")
    try:
        Execute_on_DB(add_column_query)
        Execute_on_DB(Insert_Query)
    except Exception as e:
        print(e)
        return False
    return True


def DB_get_Class_records(Standard, Section):
    ClassName = f"class{Standard}{Section}"
    Query = (f"SELECT * FROM {ClassName} WHERE Context = 'Adm_NO' OR Context = 'Name' OR Context = 'D.O.B' OR Context "
             f"= 'Gender' OR Context = 'Parent_Name' OR Context = 'Parent_NO'")
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_delete_a_student(Standard: int,Section: str,Roll_NO: int):
    ClassName = f"class{Standard}{Section}"
    Student_column = f"Roll_NO_{Roll_NO}"
    Query = f"ALTER TABLE {ClassName} DROP COLUMN {Student_column};"
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


