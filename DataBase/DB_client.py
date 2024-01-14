from datetime import datetime
from DataBase.DB_conn import Fetch_all_from_database, Fetch_par_from_database
from Security.Hash import Convert_to_hash


def DB_Validate_Parent(Standard: str, Section: str, Roll_NO: int, Password: str):
    ClassName = "class" + f"{Standard}" + f"{Section}"
    ColumnsName = f"Roll_NO_{Roll_NO}"
    Query = f"SELECT {ColumnsName}  FROM {ClassName} WHERE Context = 'Parent_PSD'"
    try:
        result = Fetch_all_from_database(Query)
        if result[0][0] == Convert_to_hash(Password):
            return True
        elif result is None:
            return None
        else:
            return False
    except Exception as e:
        print(e)
        return False


def DB_Validate_Student(Standard: str, Section: str, Roll_NO: int, Password: str):
    ClassName = "class" + f"{Standard}" + f"{Section}"
    ColumnsName = f"Roll_NO_{Roll_NO}"
    Query = f"SELECT {ColumnsName}  FROM {ClassName} WHERE Context = 'Password'"
    try:
        result = Fetch_all_from_database(Query)
        print(Password)
        if result[0][0] == Convert_to_hash(Password):
            return True
        elif result is None:
            return None
        else:
            return False
    except Exception as e:
        print(e)
        return False


def DB_Basic_Info(Standard: int, Section: str, Roll_NO: int):
    ClassName = "class" + f"{Standard}" + f"{Section}"
    ColumnsName = f"Roll_NO_{Roll_NO}"
    Query = f"SELECT Date , Context , {ColumnsName} FROM {ClassName}"
    try:
        result = Fetch_all_from_database(Query)
        if result is not None:
            return result
        else:
            return None
    except Exception as e:
        print(e)
        return False


def DB_Get_Homework(Standard: str, Section: str):
    Query = f"SELECT * FROM HomeWork_Table WHERE Standard = %s AND Section = %s"
    Values = (Standard, Section)
    try:
        result = Fetch_par_from_database(Query, Values)
        if result is not None:
            return result
        elif result is None:
            return None
    except Exception as e:
        print(e)
        return False


def DB_Fetch_Notices(Standard: str, Section: str):
    current_date = datetime.now().strftime('%Y-%m-%d')
    ClassName = "class" + f"{Standard}" + f"{Section}"
    Table_name = f"Notices_Table"
    Query = f"SELECT * FROM {Table_name} WHERE Receiver = 'ALL' OR Receiver = '{ClassName}'"
    Value = current_date
    try:
        result = Fetch_par_from_database(Query, Value)
        if result is not None:
            return result
        elif result is None:
            return None
    except Exception as e:
        print(e)
        return False


def DB_Fetch_TimeTable(Standard: int, Section: str):
    Table_name = f"Time_Table"
    Query = f"SELECT * FROM {Table_name} WHERE Standard = %s AND Section =%s"
    Values = (Standard, Section)
    try:
        Time_Table = Fetch_par_from_database(Query, Values)
        if Time_Table is not None:
            return Time_Table
        elif Time_Table is None:
            return None
    except Exception as e:
        print(e)
        return False
