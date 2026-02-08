from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Test User"}
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total