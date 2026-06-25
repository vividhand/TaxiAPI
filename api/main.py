import uvicorn
from fastapi import FastAPI
from routers.users import rt as rt_user
from routers.admins import rt as rt_admins
from routers.drivers import rt as rt_drivers
app = FastAPI()

app.include_router(router=rt_user)
app.include_router(router=rt_admins)
app.include_router(router=rt_drivers)

if "__main__" == __name__:
    uvicorn.run("main:app", reload=True, port=200)


