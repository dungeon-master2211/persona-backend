
from google.genai import types, Client
from prompts.llm_prompts import PERSONA_BASED_PROMPT, AI_GIRL
from Body_Schema.response_body import LLM_Chat_response_Model
SYSTEM_PROMPT = AI_GIRL

def start_chat(gemini_client:Client,user_input,history=[]):
    
    chat = gemini_client.chats.create(
        model="gemini-2.0-flash",
        history = history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema = LLM_Chat_response_Model
            ),
        )
    response = chat.send_message(message=user_input,)
    print(response.text)
    return response.text
    # while True:
    #     user_input = input("> ")
    #     response = chat.send_message(message=user_input)
    #     print(response.text)
        

