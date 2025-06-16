from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,HTTPException
from app.routes import file,graph,dashboard
from app.auth import auth
import uvicorn

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file.router)
app.include_router(auth.router,prefix="/auth", tags=["auth"])
app.include_router(graph.router)
app.include_router(dashboard.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

