import uvicorn
from fastapi import FastAPI
from routers import rt_drivers, rt_auth, rt_users, rt_admins
app = FastAPI()
app.include_router(router=rt_users)
app.include_router(router=rt_admins)
app.include_router(router=rt_drivers)
app.include_router(router=rt_auth)

if "__main__" == __name__:
    uvicorn.run("main:app", port=200)