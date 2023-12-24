from pydantic import BaseModel


class Homework_Model(BaseModel):
    Standard: int
    Section: str
    Subject: str
    Day: str
    Homework: str
