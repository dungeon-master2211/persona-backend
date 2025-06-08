from pydantic import BaseModel

class LLM_Chat_response_Model(BaseModel):
    response: str