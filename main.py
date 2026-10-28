from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.src.db.database import init_db
from backend.src.routes.allRoutes import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
init_db()
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the first flaskapi project"}

# Run the application on port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
