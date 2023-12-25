from datetime import datetime
from DataBase.DB_conn import Execute_on_DB, Fetch_all_from_database, Insert_on_DB, Check_Table_Exist
from Models.Admin_schemas import StudentModel, TeacherModel, TimeTableModel, Notices_Model
from Security.Hash import Convert_to_hash


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
    Student.Password = Convert_to_hash(Student.Password)
    Student.Parent_PSD = Convert_to_hash(Student.Parent_PSD)
    ClassName = f"class{Student.Standard}{Student.Section}"
    ColumnsName = f"Roll_NO_{Student.Roll_NO}"
    add_column_query = f"ALTER TABLE {ClassName} ADD COLUMN IF NOT EXISTS {ColumnsName} TEXT"

    insert_query = (f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Adm_NO';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Name';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'D.O.B';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Gender';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Parent_Name';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Parent_NO';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Password';"
                    f"UPDATE {ClassName} SET {ColumnsName} = %s WHERE Context = 'Parent_PSD';")

    values = (Student.Adm_NO, Student.Name, Student.DOB, Student.Gender,
              Student.Parent_Name, Student.Parent_NO, Student.Password, Student.Parent_PSD)
    try:
        Execute_on_DB(add_column_query)
        Insert_on_DB(insert_query, values)
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


def DB_delete_a_student(Standard: int, Section: str, Roll_NO: int):
    ClassName = f"class{Standard}{Section}"
    Student_column = f"Roll_NO_{Roll_NO}"
    Query = f"ALTER TABLE {ClassName} DROP COLUMN {Student_column};"
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


# ----------------------------------------------------------------
# Teacher Functions

def Create_Teacher_Table():
    Table_name = f"Teacher_Table"
    Query = f"""CREATE TABLE IF NOT EXISTS {Table_name} (
        Name VARCHAR(30),
        ID INTEGER,
        Password VARCHAR(255),
        Standard INT,
        Section VARCHAR(6),
        Subject VARCHAR(10),
        Contact_NO VARCHAR(15),
        Other_Classes VARCHAR(50),
        Degree VARCHAR(20)
    );
    """
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


def DB_Add_Teacher(Teacher: TeacherModel):
    Teacher.Password = Convert_to_hash(Teacher.Password)
    if Check_Table_Exist("Teacher_Table"):
        pass
    else:
        try:
            Create_Teacher_Table()
        except Exception as e:
            print(e)
            return False
    Query = """
    INSERT INTO Teacher_records (Name, ID, Password, Standard, Section, Subject, Contact_NO, Other_Classes, Degree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    Values = (
        Teacher.Name,
        Teacher.ID,
        Teacher.Password,
        Teacher.Standard,
        Teacher.Section,
        Teacher.Subject,
        Teacher.Contact_NO,
        Teacher.Other_Classes,
        Teacher.Degree
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True


def DB_Get_Teachers():
    Table_name = f"Teacher_Table"
    Query = f"SELECT * FROM {Table_name}"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_delete_Teacher(ID: int):
    Table_name = f"Teacher_Table"
    Query = f"DELETE FROM {Table_name} WHERE ID = {ID}"
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return True
    return False


# ----------------------------------------------------------------
# Time_Table Functions


def Create_Time_Table():
    Table_name = f"Time_Table"
    Query = f"""CREATE TABLE IF NOT EXISTS {Table_name} (
            Standard VARCHAR(10),
            Section INTEGER,
            Weekday VARCHAR(30),
            Lect_1 INTEGER,
            Lect_2 INTEGER,
            Lect_3 INTEGER,
            Lect_4 INTEGER,
            Lect_5 INTEGER,
            Lect_6 INTEGER,
            Lect_7 INTEGER,
            Lect_8 INTEGER
            );"""
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


def DB_add_Time_Table(Time_Table: TimeTableModel):
    if Check_Table_Exist("Time_Table"):
        pass
    else:
        try:
            Create_Time_Table()
        except Exception as e:
            print(e)
            return False
    Query = """
    INSERT INTO Time_Table (Standard, Section, Weekday, Lect_1, Lect_2, Lect_3, Lect_4, Lect_5, Lect_6, Lect_7, Lect_8)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    Values = (
        Time_Table.Standard,
        Time_Table.Section,
        Time_Table.Weekday,
        Time_Table.Lect_1,
        Time_Table.Lect_2,
        Time_Table.Lect_3,
        Time_Table.Lect_4,
        Time_Table.Lect_5,
        Time_Table.Lect_6,
        Time_Table.Lect_7,
        Time_Table.Lect_8
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True


def DB_delete_time_table(Standard: int, Section: str, Weekday: str):
    Table_name = f"Time_Table"
    Query = f"DELETE FROM {Table_name} WHERE Standard = {Standard} AND Section = {Section} AND Weekday = {Weekday}"
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return True
    return False


def DB_get_time_tale(Standard: int, Section: str):
    Table_name = f"Time_Table"
    Query = f"SELECT * FROM {Table_name} WHERE Standard = {Standard} AND Section = {Section}"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


# ----------------------------------------------------------------
# Notices Routes

def DB_create_notices_table():
    Table_name = f"Notices_Table"
    Query = f"""CREATE TABLE IF NOT EXISTS {Table_name} (
            Sr_no SERIAL PRIMARY KEY,
            Title VARCHAR(20),
            Heading VARCHAR(45),
            Description VARCHAR(250),
            Send_DATE DATE,
            For_Date DATE,
            Receiver VARCHAR(10)
            );"""
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


def DB_add_Notice(Notice: Notices_Model):
    Table_name = f"Notices_Table"
    if Check_Table_Exist(Table_name):
        pass
    else:
        try:
            DB_create_notices_table()
        except Exception as e:
            print(e)
            return False
    current_date = datetime.now().strftime('%Y-%m-%d')
    Receiver = "ALL"
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


def DB_delete_Notice(Sr_no: int):
    Table_name = f"Notices_Table"
    Query = f"DELETE FROM {Table_name} WHERE Sr_no ={Sr_no}"
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return True
    return False


def DB_get_Notices():
    Table_name = f"Notices_Table"
    Query = f"SELECT * FROM {Table_name} ORDER BY Sr_no"
    try:
        Data = Fetch_all_from_database(Query)
    except Exception as e:
        print(e)
        return False
    return Data


def DB_Create_HW_Table():
    Query = """
    CREATE TABLE IF NOT EXISTS HomeWork_Table (
        ID SERIAL PRIMARY KEY,
        Standard VARCHAR(10) NOT NULL,
        Section VARCHAR(10) NOT NULL,
        Subject VARCHAR(100) NOT NULL,
        Monday TEXT DEFAULT 'yet to be added',
        Tuesday TEXT DEFAULT 'yet to be added',
        Wednesday TEXT DEFAULT 'yet to be added',
        Thursday TEXT DEFAULT 'yet to be added',
        Friday TEXT DEFAULT 'yet to be added',
        Saturday TEXT DEFAULT 'yet to be added'
    )
    """
    try:
        Execute_on_DB(Query)
    except Exception as e:
        print(e)
        return False
    return True


def DB_Config_HW_Table(Standard, Section, Subject):
    Query = """
    INSERT INTO HomeWork_Table (Standard, Section, Subject)
    VALUES (%s, %s, %s)
    """
    Values = (
        Standard, Section, Subject
    )
    try:
        Insert_on_DB(Query, Values)
    except Exception as e:
        print(e)
        return False
    return True
