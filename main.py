from fastapi import FastAPI
from DataBase.DB_conn import Check_DB_Connection
from Routers.admin_routers import router as admin_routers
from Routers.teacher_routers import router as teacher_routers
from Routers.client_routers import router as client_routers
from Routers.general_purpose import router as general_purpose_routers

app = FastAPI()


@app.get("/")
def BaseRoot():
    print("yes prints")
    return {"Backend": "Working"}


@app.get("/Check_DB_Connection")
def Check_Connection():
    if Check_DB_Connection():
        return {"Connection": "Working"}
    else:
        return {"Connection": "Hampered"}


app.include_router(admin_routers, prefix="/Admin")
app.include_router(teacher_routers, prefix="/Teacher")
app.include_router(client_routers, prefix="/Client")
app.include_router(general_purpose_routers, prefix="/gen")
