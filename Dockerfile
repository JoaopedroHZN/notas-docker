# Imagem Oficial e enxuta
FROM python:3.12-slim

# diretorio de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependenciaas
# 

COPY requirements.txt .

# instalaa as dependencias listadas no arquivo
RUN pip install --no-cache-dir -r requirements.txt

# copia o resto do codigo
COPY . .

# declara a variavel de ambiente 
ENV DATA_DIR=/app/data

# porta q o container vai escutar
EXPOSE 8000


# Declara q o /app/data e um volume e isso sinaliza para o docker q os dados salvos aq nao devem ser perdidos quando o container morrer
VOLUME /app/data

# comando para iniciar o servidor na porta 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]