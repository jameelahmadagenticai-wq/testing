from fastapi import FastAPI 

from app.routers.users import router as user_router

from app.routers.todos import router as todo_router


app = FastAPI(title = "Todo API")

@app.get("/")
def home():
    return {"message": "FastAPI is running "}

app.include_router(user_router)
app.include_router(todo_router)
