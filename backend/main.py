from fastapi import FastAPI

from services.serviceia import ask_ai

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "AI Business Assistant API funcionando"
    }


@app.get("/preguntar")
def preguntar(prompt: str):
    respuesta = ask_ai(prompt)

    return respuesta