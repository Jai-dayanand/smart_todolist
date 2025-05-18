from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoOut(TodoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
