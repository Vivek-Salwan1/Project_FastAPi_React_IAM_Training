from fastapi import FastAPI,HTTPException,status
from db.database import init_db

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the first flaskapi project"}

