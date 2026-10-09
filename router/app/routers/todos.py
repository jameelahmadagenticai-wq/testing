from fastapi import APIRouter , HTTPException
from app.database import todos
from app.schemas.todo import TodoCreate


router = APIRouter(
    prefix = "/todos",
    tags=["Todos"]
)


@router.get("/")
def get_todos():
    return todos

@router.post("/")
def create_todo(todo: TodoCreate):
    new_todo={
        "id": len(todos) + 1,
        **todo.model_dump()


    }

    todos.append(new_todo)
    return new_todo


@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate):

    for item in todos:
        if item["id"] == todo_id:
            item.update(todo.model_dump())
            return item

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


    
@router.delete("/{todo_id}")
def delete_todo(todo_id:int):
    for index , item in enumerate(todos):
        if item["id"] == todo_id:
            todos.pop(index)

            return{
                "message": "Todo deleted"
            }

    raise HTTPException(
        status_code = 404,
        detail = "todo not found"
    )