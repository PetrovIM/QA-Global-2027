from fastapi import FastAPI
from pydantic import BaseModel
from sql.db_client import DBClient

app = FastAPI()
db = DBClient()
db.connect_db()

class User(BaseModel):
    username: str
    email: str
    age: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users")
def create_user(user: User):
    user_model = user.model_dump()
    value = (user_model["username"], user_model["email"], user_model["age"])
    db.insert_db("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)", value)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    value = (user_id,)
    user = db.select_db("SELECT * FROM users WHERE id= %s", value)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    value = (user_id,)
    db.delete_db("DELETE FROM users WHERE id= %s", value)
    return {"status": "DELETED"}