
from fastapi import FastAPI,HTTPException
from app.routes import file,user,secure
from app.auth import auth
import uvicorn

app = FastAPI()
app.include_router(file.router)
# app.include_router(secure.router)
app.include_router(auth.router,prefix="/auth")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

