from fastapi import APIRouter , HTTPException

from app.database import users
from app.schemas.user import UserCreate

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/")
def get_users():
    return users



@router.post("/")
def create_user(user: UserCreate):
    new_user={
        "id": len(users) + 1,
        **user.model_dump()
    }

    users.append(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
         return user
    
    raise HTTPException(
       status_code = 404,
       detail = "User not found"

    )