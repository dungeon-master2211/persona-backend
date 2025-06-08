from pydantic import BaseModel

class Chat_Router_Body(BaseModel):
    id: int|str
    question: str | None