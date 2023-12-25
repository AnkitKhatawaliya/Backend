from pydantic import BaseModel


class Homework_Model(BaseModel):
    Standard: int
    Section: str
    Subject: str
    Day: str
    Homework: str


class Notices_Model(BaseModel):
    Title: str
    Heading: str
    Description: str
    for_date: str
    Standard: int
    Section: str
