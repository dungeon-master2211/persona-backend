from typing import Annotated
from fastapi import Depends, Request
from google import genai
def get_gemini_client(request:Request):
    gemini_client = request.app.state.gemini_client
    return gemini_client

gemini_client_dependency = Annotated[genai.Client,Depends(get_gemini_client)]