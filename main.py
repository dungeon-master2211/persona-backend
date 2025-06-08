from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.chat_router import chat_router
from dotenv import load_dotenv
from google import genai
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create gemini client
    client = genai.Client(api_key=GEMINI_API_KEY) 
    app.state.gemini_client = client
    yield
    
app = FastAPI(title="Persona Chat", lifespan= lifespan)

origins = [
    "http://localhost:5173",
    "https://persona-frontend-psi.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
@app.get('/')
def health_check():
    return {'content':'working'}

