from google import genai
from google.genai import types
from pydantic import BaseModel
from enum import Enum
from services.tools import consultar_cliente
from services.tools import consultar_servicios
from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"}
)


SYSTEM_PROMPT = """
Sos un asistente virtual para empresas.

Tu objetivo es ayudar a los usuarios a resolver consultas
relacionadas con negocios, clientes, servicios y tareas administrativas.

Reglas:
- Respondé siempre en español.
- Sé claro y profesional.
- No inventes información.
- Si no tenés suficiente información, indicá que necesitás más datos.
- Priorizá respuestas concretas y fáciles de entender.
"""


class Intent(str, Enum):
    CONSULTAR_SERVICIOS = "consultar_servicios"
    CREAR_SOLICITUD = "crear_solicitud"
    CONSULTAR_SOLICITUD = "consultar_solicitud"
    CONSULTAR_CLIENTE = "consultar_cliente"
    OTRO = "otro"


class AIResponse(BaseModel):
    intencion: Intent
    respuesta: str


consultar_servicios_tool = {
    "type": "function",
    "name": "consultar_servicios",
    "description": "Consulta los servicios que ofrece la empresa.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

consultar_cliente_tool = {
    "type": "function",
    "name": "consultar_cliente",
    "description": "Busca información de un cliente por su nombre.",
    "parameters": {
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string",
                "description": "Nombre completo del cliente."
            }
        },
        "required": ["nombre"]
    }
}

def ask_ai(prompt: str):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        system_instruction=SYSTEM_PROMPT,
        tools=[
            consultar_servicios_tool,
            consultar_cliente_tool
        ]
    )

    for step in interaction.steps:

        if step.type == "function_call":

            if step.name == "consultar_servicios":
                resultado = consultar_servicios()

            elif step.name == "consultar_cliente":
                nombre = step.arguments["nombre"]
                resultado = consultar_cliente(nombre)

            else:
                continue

            final_interaction = client.interactions.create(
                model="gemini-3.6-flash",
                previous_interaction_id=interaction.id,
                input=[
                    {
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": str(resultado)
                            }
                        ]
                    }
                ]
            )

            return {
                "tipo": "respuesta",
                "respuesta": final_interaction.output_text
            }

    return {
        "tipo": "respuesta",
        "respuesta": interaction.output_text
    }