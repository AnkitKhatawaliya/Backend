from fastapi import FastAPI
from DataBase.DB_conn import Check_DB_Connection
# from Routers.admin_routers import router as admin_routers
from Routers.teacher_routers import router as teacher_routers

app = FastAPI()


@app.get("/")
def BaseRoot():
    return {"Backend": "Working"}


@app.get("/Check_DB_Connection")
def Check_Connection():
    if Check_DB_Connection():
        return {"Connection": "Working"}
    else:
        return {"Connection": "Hampered"}


# app.include_router(admin_routers, prefix="")
app.include_router(teacher_routers, prefix="")
