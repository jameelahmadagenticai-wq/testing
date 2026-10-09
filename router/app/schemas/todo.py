from pydantic import BaseModel

class TodoCreate(BaseModel):
    title:str 
    completed:bool = False