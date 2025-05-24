cat > mcp_server.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

def agente_sped(input_text: str) -> str:
    return f"[Agente SPED] Analisando questão fiscal: '{input_text}'"

def agente_sistema(input_text: str) -> str:
    return f"[Agente Sistema] Respondendo dúvida sobre o Transmitiu: '{input_text}'"

class PerguntaRequest(BaseModel):
    input: str
    user_id: str
    conversation_id: str

class RotaResponse(BaseModel):
    route: Literal["SPED", "SISTEMA"]

class RespostaAgente(BaseModel):
    resposta: str

@app.post("/agent/orquestrador", response_model=RotaResponse)
def orquestrador(req: PerguntaRequest):
    texto = req.input.lower()
    if any(p in texto for p in ["cfop", "cst", "sped", "registro", "bloco", "validação", "nota fiscal"]):
        return {"route": "SPED"}
    if any(p in texto for p in ["tela", "erro de sistema", "login", "plano", "transmitiu", "senha", "envio"]):
        return {"route": "SISTEMA"}
    return {"route": "SPED"}

@app.post("/agent/sped", response_model=RespostaAgente)
def agente_sped_endpoint(req: PerguntaRequest):
    resposta = agente_sped(req.input)
    return {"resposta": resposta}

@app.post("/agent/sistema", response_model=RespostaAgente)
def agente_sistema_endpoint(req: PerguntaRequest):
    resposta = agente_sistema(req.input)
    return {"resposta": resposta}
EOF