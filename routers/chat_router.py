from collections import defaultdict
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from google.genai import types
from llm_utils.gemini_chat import start_chat
from Body_Schema.request_body import Chat_Router_Body
from dependency import gemini_client_dependency
import json
import uuid

chat_router = APIRouter()

inmemory_history = defaultdict(list)

@chat_router.get("/session-id")
def get_session_id():
    i=0
    while i<5:
        new_id = str(uuid.uuid4())
        if len(inmemory_history[new_id])==0:
            return {"message":new_id}
        i+=1
    raise HTTPException(status_code=400,detail='Could not establish session. Try Again')

@chat_router.post('/chat')
def chat_route(body:Chat_Router_Body,gemini_client:gemini_client_dependency):
    user_prompt = body.question
    user_id = body.id

    if user_prompt is None: 
        return HTTPException(status_code=400, content="Please ask a question")

    user_history = inmemory_history.get(user_id,[])[:-100:-1][::-1]
    print(user_history)
    # add user prompt into inmemry dict
    inmemory_history[user_id].append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_prompt)]
    ))

    response = start_chat(gemini_client=gemini_client,user_input=user_prompt,history=user_history)

    content = json.loads(response)
    inmemory_history[user_id].append(types.Content(
        role= "model",
        parts= [types.Part.from_text(text=content.get("response"))]
        )
    )

    return JSONResponse(status_code=200,content=content)