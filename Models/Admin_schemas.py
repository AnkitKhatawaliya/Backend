from pydantic import BaseModel


class AdminLogin(BaseModel):
    ID: str
    Password: str


class Class_Table(BaseModel):
    Standard: int
    Section: str


class StudentModel(BaseModel):
    Standard: int
    Section: str
    Roll_NO: int
    Adm_NO: int
    Name: str
    DOB: str
    Gender: str
    Parent_Name: str
    Parent_NO: str
    Password: str
    Parent_PSD: str


class TeacherModel(BaseModel):
    Name: str
    ID: int
    Password: str
    Standard: int
    Section: str
    Subject: str
    Contact_NO: str
    Other_Classes: str
    Degree: str


class TimeTableModel(BaseModel):
    Standard: int
    Section: str
    Weekday: str
    Lect_1: int
    Lect_2: int
    Lect_3: int
    Lect_4: int
    Lect_5: int
    Lect_6: int
    Lect_7: int
    Lect_8: int


# class ExampleModel(BaseModel):
#     integer_value: int
#     float_value: float
#     boolean_value: bool
#     list_of_integers: List[int]
#     dictionary_of_strings: Dict[str, str]
#     tuple_of_strings_and_int: Tuple[str, int]
#     set_of_floats: Set[float]
#     any_value: Any
#
# # Example instantiation
# data = {
#     'integer_value': 42,
#     'float_value': 3.14,
#     'boolean_value': True,
#     'list_of_integers': [1, 2, 3],
#     'dictionary_of_strings': {'key1': 'value1', 'key2': 'value2'},
#     'tuple_of_strings_and_int': ('text', 123),
#     'set_of_floats': {1.23, 4.56, 7.89},
#     'any_value': 'anything'
# }
