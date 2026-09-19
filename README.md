# 📝 Notas API (Docker & FastAPI)

Uma API simples em Python construída com **FastAPI** para gerenciar anotações em texto. Este projeto foi concebido para demonstrar a conteinerização de aplicações web e como funciona a **persistência de dados** em contêineres utilizando *Docker Volumes*.

## ✨ Funcionalidades

- **Criar notas:** Salve suas anotações enviando requisições via POST.
- **Listar notas:** Recupere todo o histórico de notas salvas.
- **Health Check:** Endpoint simples para checar a disponibilidade da API.
- **Persistência Segura:** Utiliza volumes do Docker para que suas informações não se percam quando o contêiner é reiniciado ou apagado.

## 🛠️ Tecnologias Utilizadas

- [Python 3.12](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)

---

## 🚀 Como Executar

Certifique-se de ter o **Docker** instalado na sua máquina.

### 1. Construir a imagem Docker

Na raiz do repositório, execute o comando para buildar a imagem:

```bash
docker build -t notas-api:1.0 .
```

### 2. Criar o volume de dados

Para não perder suas notas quando o contêiner for destruído, crie um volume no Docker:

```bash
docker volume create notas-dados
```

### 3. Iniciar o contêiner

Inicie o serviço mapeando uma porta do Host (por exemplo, 9000) para a porta interna (8000) e atrelando o volume de dados na pasta onde o app salva as informações (`/app/data`):

```bash
docker run -d \
  --name notas-api-container \
  -p 9000:8000 \
  -v notas-dados:/app/data \
  notas-api:1.0
```

Se o contêiner inicializou com sucesso, a API já estará disponível em `http://localhost:9000`.

---

## 📖 Endpoints da API

Como utilizamos FastAPI, você pode acessar a **Documentação Interativa (Swagger)** pelo próprio navegador em: 
👉 **`http://localhost:9000/docs`**

Abaixo estão os endpoints disponíveis caso queira usar via terminal (`curl`) ou ferramentas como Postman/Insomnia:

### 🔹 Health Check
Verifica se o servidor web está online.
* **GET** `/health`

*Resposta esperada:*
```json
{
  "status": "ok"
}
```

### 🔹 Listar Anotações
Retorna a lista completa com todas as notas gravadas.
* **GET** `/notas`

*Resposta esperada:*
```json
[
  {
    "texto": "Minha primeira nota salva!",
    "data_hora": "2026-09-18T20:55:00.123456"
  }
]
```

### 🔹 Criar Nova Anotação
Insere uma anotação nova no banco. O servidor captura a data e a hora do momento automaticamente.
* **POST** `/notas`

*Body (JSON):*
```json
{
  "texto": "Estudar mais sobre Docker Volumes"
}
```

---

## 📂 Persistência e Efemeridade

A variável de ambiente padrão configurada na API para salvar o arquivo `notas.json` é a `/app/data`. 

Caso você inicie o contêiner **sem** a flag `-v notas-dados:/app/data` e por algum motivo ele seja removido, **todas as suas anotações serão perdidas**, já que o sistema de arquivos interno de um contêiner é efêmero por padrão. O uso de Volumes é vital para resolver isso e jogar a persistência diretamente para o seu Host físico.

*Para ler a análise técnica detalhada da atividade, confira o [Relatório](RELATORIO.md) no repositório.*
