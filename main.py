from fastapi import FastAPI,HTTPException,status

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the first flaskapi project"}

