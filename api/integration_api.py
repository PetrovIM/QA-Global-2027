from fastapi import FastAPI
from pydantic import BaseModel
from sql.db_client import DBClient

app = FastAPI()
db = DBClient()

class User(BaseModel):
    username: str
    email: str
    age: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users")
def create_user(user: User):

    return user