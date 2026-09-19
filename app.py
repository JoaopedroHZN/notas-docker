import os
import json
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DATA_DIR = os.getenv("DATA_DIR", "/app/data")

NOTAS_FILE = os.path.join(DATA_DIR, "notas.json")

# funcao pra garantir q o diretorio e o json existam
def init_db():
    # cria a pasta caso nao exista
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # e cria o notas.json com lista vazia caso nao exista
    if not os.path.exists(NOTAS_FILE):
        with open (NOTAS_FILE, "w") as f:
            json.dump([], f)

# quando recebe post ele espera um json com o campo texto
class Nota(BaseModel):
    texto: str

# inicia o bd
init_db()

# rota Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# rota para ver todas as anotacoes
@app.get("/notas")
def listar_notas():

    try:
        # abre o json em leitura e retorna o conteudo
        with open(NOTAS_FILE, "r") as f:
            notas = json.load(f)
        return notas

    except Exception as e:
        # se der errado ele retorna uma lista vazia
        return []


# rota para criar anotacao
@app.post("/notas")
def criar_nota(nota: Nota):
    # le as notas atuais
    with open (NOTAS_FILE, "r") as f:
        notas = json.load(f)

    # monta a nota nova e adiciona data e hora atual
    nova_nota = {
        "texto": nota.texto,
        "data_hora": datetime.now().isoformat()
    }


    # adiciona a nova nota
    notas.append(nova_nota)

    # e salva a lista completa no json com o W
    with open(NOTAS_FILE, "w") as f:
        json.dump(notas, f, indent=4)

    return nova_nota