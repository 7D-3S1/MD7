from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from chainlit.context import init_http_context
import chainlit as cl


app = FastAPI()

@app.get("/app")
async def read_main():
    init_http_context()
    await cl.Message(content="Hello, I am a chatbot!").send()
    return {"message": "Hello World from main app"}

# pass path="" to mount the Chainlit app on the root path
mount_chainlit(app=app, target="web.py", path="/chainlit")
