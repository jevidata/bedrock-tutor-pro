'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import boto3
import json

from backend.retrieval import ChunkRetriever

# -------------------------------------------------
# Configuración de FastAPI y CORS
# -------------------------------------------------

app = FastAPI(title="Bedrock Tutor Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # En producción se debería restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Cliente de Amazon Bedrock (preparado para futuro)
# -------------------------------------------------

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

# ID del modelo Amazon Nova Lite 1.0 en Bedrock
NOVA_MODEL_ID = "amazon.nova-lite-v1:0"

# -------------------------------------------------
# Recuperador de fragmentos
# -------------------------------------------------

retriever = ChunkRetriever()

def build_prompt(question: str) -> str:
    # 1) Recuperar fragmentos relevantes
    chunks = retriever.retrieve(question, top_k=5)

    context_parts = []
    for ch in chunks:
        context_parts.append(f"- [{ch['doc_id']}] {ch['text']}")
    context_text = "\n".join(context_parts)

    # 2) Construir el prompt para Nova Lite
    prompt = (
        "Eres un tutor virtual para el alumnado del Curso de Especialización "
        "en Inteligencia Artificial y Big Data en la Comunidad Valenciana. "
        "Debes responder solo usando la información de los documentos oficiales "
        "(Real Decreto, ficha del Ministerio y documentación de la Generalitat Valenciana). "
        "Si algo no aparece en estos documentos, indica que no dispones de esa información.\n\n"
        "Documentación relevante:\n"
        f"{context_text}\n\n"
        f"Pregunta del alumno: {question}\n\n"
        "Respuesta clara y breve:"
    )
    print(prompt)
    return prompt

def call_bedrock_nova(messages: list[dict]) -> str:
    body = {
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": 256,
            "temperature": 0.3,
        },
    }

    response = bedrock_client.invoke_model(
        modelId=NOVA_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read())

    try:
        return response_body["output"]["message"]["content"][0]["text"]
    except Exception:
        return json.dumps(response_body, ensure_ascii=False)


# -------------------------------------------------
# Modelos de datos de la API
# -------------------------------------------------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

# -------------------------------------------------
# Endpoints de la API
# -------------------------------------------------

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bedrock Tutor Pro API funcionando"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.message
    prompt = build_prompt(question)

    # Temporal: no llamar aún a Bedrock
    # messages = [{"role": "user", "content": prompt}]
    # answer = call_bedrock_nova(messages)

    answer = (
        "Respuesta simulada. El backend ha recuperado documentación relevante "
        "y construiría aquí la respuesta usando Amazon Bedrock."
    )

    return ChatResponse(answer=answer)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.message
    prompt = build_prompt(question)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt,
                }
            ],
        }
    ]

    # Llamada real a Amazon Nova Lite
    answer = call_bedrock_nova(messages)

    return ChatResponse(answer=answer)

'''
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

# -------------------------------------------------
# Configuración de FastAPI y CORS
# -------------------------------------------------
app = FastAPI(title="Bedrock Tutor Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Cliente de Amazon Bedrock AGENT
# -------------------------------------------------
# Usamos 'bedrock-agent-runtime' para hablar con el Agente que creamos
agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# --- CONFIGURACIÓN DEL AGENTE ---
# Sustituye este ID por el tuyo (está en la consola de Bedrock -> Detalles del agente)
AGENT_ID = "ZZR8GWAMJJ" 
AGENT_ALIAS_ID = "TSTALIASID"  # Mantenlo así para usar el borrador actual

# -------------------------------------------------
# Modelos de datos de la API
# -------------------------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

# -------------------------------------------------
# Endpoints de la API
# -------------------------------------------------

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bedrock Tutor Pro API con Agente activa"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.message
    
    try:
        # Invocamos al agente directamente. Él ya sabe leer los PDFs.
        response = agent_client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId="sesion_unica_tutor", # Identificador de la charla
            inputText=question
        )

        answer = ""
        # El agente devuelve la respuesta por trozos (stream)
        for event in response.get("completion"):
            chunk = event.get("chunk")
            if chunk:
                answer += chunk.get("bytes").decode("utf-8")
        
    except Exception as e:
        answer = f"Error conectando con el agente: {str(e)}"

    return ChatResponse(answer=answer)
    
'''
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import uuid

# 1. Configuración de FastAPI
app = FastAPI(title="Bedrock Tutor Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Cliente de Bedrock
agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

AGENT_ID = "ZZR8GWAMJJ" 
AGENT_ALIAS_ID = "TSTALIASID" 

# 3. Modelos de datos
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

# 4. Endpoints
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API Activa"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.message
    # Generamos un ID de sesión único por cada pregunta para evitar respuestas cortadas
    session_id = str(uuid.uuid4())
    
    try:
        response = agent_client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=question
        )
        
        full_answer = ""
        # Recorremos el stream de eventos de Bedrock
        for event in response.get("completion", []):
            if "chunk" in event:
                chunk_bytes = event["chunk"].get("bytes", b"")
                full_answer += chunk_bytes.decode("utf-8")
        
        # Si después de todo el bucle la respuesta está vacía
        if not full_answer:
            full_answer = "El agente no encontró información relevante en la base de conocimientos."

    except Exception as e:
        full_answer = f"Error conectando con el agente de AWS: {str(e)}"

    return ChatResponse(answer=full_answer)
fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
'''
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Configuración de la App
app = FastAPI(title="Bedrock Tutor Pro API")

# 2. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Cliente de AWS Bedrock
agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# IDs de configuración
AGENT_ID = "ZZR8GWAMJJ" 
AGENT_ALIAS_ID = "TSTALIASID" 

# 4. Modelos de Datos
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

# 5. Rutas
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API Activa y lista para el Tutor"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Definimos la variable que viene del usuario
    question = request.message
    session_id = "user-session-tutor-pro"
    
    try:
        # Llamada al agente usando los nombres de parámetros exactos y la variable 'question'
        response = agent_client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=question,
            enableTrace=False,
            endSession=False
        )
        
        full_answer = ""
        # Procesar la respuesta por fragmentos (chunks)
        for event in response.get("completion", []):
            if "chunk" in event:
                chunk_bytes = event["chunk"].get("bytes", b"")
                full_answer += chunk_bytes.decode("utf-8")
        
        if not full_answer:
            full_answer = "El agente no encontró información específica en los documentos."

    except Exception as e:
        print(f"Error detectado: {str(e)}")
        full_answer = f"Error de conexión con AWS: {str(e)}"

    return ChatResponse(answer=full_answer)
