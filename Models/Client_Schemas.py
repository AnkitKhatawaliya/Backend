from pydantic import BaseModel

class Validation_Model(BaseModel):
    Roll_NO: int
    Password: str
    Standard: int
    Section: str
    Role: str
