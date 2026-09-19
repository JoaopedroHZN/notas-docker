# Relatório: Implementação de Serviços com Docker
**Disciplina/Atividade:** Atividade Prática — Implementação de Serviços com Docker e Persistência de Dados
**Alunos:** João Pedro Montelo Menezes e Lucas Jardim 



## 1. Explicação do Dockerfile

Abaixo está o `Dockerfile` criado para a aplicação, com a explicação linha a linha das decisões tomadas para garantir uma imagem otimizada:

*   **`FROM python:3.12-slim`**: Partimos da imagem oficial do Python na variante `slim`. Isso garante um contêiner mais leve, enxuto e seguro, contendo apenas o essencial para rodar o Python, diferente da versão padrão que traz ferramentas desnecessárias.
*   **`WORKDIR /app`**: Define o diretório de trabalho padrão dentro do contêiner. Todos os comandos seguintes serão executados dentro desta pasta.
*   **`COPY requirements.txt .`**: Copiamos APENAS o arquivo de dependências primeiro. Esta é uma boa prática fundamental para o uso inteligente do cache de camadas do Docker.
*   **`RUN pip install --no-cache-dir -r requirements.txt`**: Instalamos as dependências. O uso da flag `--no-cache-dir` evita que o pip salve arquivos temporários inúteis dentro da imagem, mantendo-a menor. Como as dependências raramente mudam, esta camada fica em cache.
*   **`COPY . .`**: Após a instalação das bibliotecas, copiamos o restante do código (`app.py`, etc.). Se alterarmos apenas o código da aplicação, o Docker reconstruirá apenas esta camada e a seguinte, economizando tempo no build.
*   **`ENV DATA_DIR=/app/data`**: Declaramos a variável de ambiente exigida, definindo o caminho padrão onde os dados da aplicação serão salvos.
*   **`EXPOSE 8000`**: Documenta e sinaliza que o contêiner escutará tráfego na porta 8000.
*   **`VOLUME /app/data`**: Informa ao Docker que o diretório `/app/data` deve ser tratado como um volume, indicando que os dados persistidos ali não devem seguir o ciclo de vida efêmero do contêiner.
*   **`CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`**: O comando executado ao iniciar o contêiner, subindo o servidor FastAPI na porta exposta.

---

## 2. Evidências de Execução (Etapas 3 a 6)

### Etapa 3: Build da Imagem
*(Cole aqui o print do tamanho da imagem `docker image ls` e da lista de camadas `docker history notas-api:1.0`)*

### Etapa 4 e 5: Prova de Persistência
Criamos o volume `notas-dados`, subimos o contêiner inicial e inserimos as notas via POST. Após confirmar o funcionamento, o contêiner foi **destruído completamente** (`docker rm notas`).
Ao instanciar um novo contêiner mapeado para o mesmo volume, verificamos que os dados continuavam intactos:
*(Cole aqui o print do comando `curl http://localhost:9000/notas` retornando o JSON completo no contêiner notas2)*

### Etapa 6: O Contraexemplo (Efemeridade)
Para demonstrar o comportamento padrão de contêineres, instanciamos a aplicação sem a flag `-v`. Após inserir dados e excluir o contêiner, um novo contêiner foi criado. 
Ao realizar o GET, ficou comprovado que **as anotações foram perdidas** e o sistema retornou ao estado original da imagem. 

**Por que isso acontece?**
O sistema de arquivos de um contêiner é efêmero. A camada de leitura/escrita acoplada ao contêiner durante a execução é descartada automaticamente pelo Docker Engine quando o contêiner é removido. Sem um volume (que reside fora dessa camada e é gerenciado diretamente no *host*), a persistência é impossível.

---
README
## 3. Inspeção (Etapa 7)

**Onde, no host, o Docker armazena fisicamente o volume `notas-dados`?**README
Através do comando `docker volume inspect`, identificamos no campo `Mountpoint` que o Docker gerencia fisicamente este volume no seguinte diretório do Host: 
`/var/lib/docker/volumes/notas-dados/_data`

**Qual é o conteúdo do diretório `/app/data` dentro do contêiner?**
Executando `docker exec notas2 ls -la /app/data`, verificamos a existência do arquivo de persistência:
`-rw-rw-r-- 1 root root 444 Sep 19 00:04 notas.json`

**O que acontece com os dados se você executar `docker volume rm notas-dados` com o contêiner parado e removido?**
Ao executar este comando, os dados são apagados permanentemente. O Docker remove o volume gerenciado e apaga fisicamente a pasta `/var/lib/docker/volumes/notas-dados/_data` do disco rígido da máquina Host.

---

## 4. Dificuldades e Aprendizados

A principal dificuldade encontrada durante a atividade foi o conflito de portas ("address already in use"). Como portas de desenvolvimento comuns (como 8000 e 8080) já estavam retidas por outros processos no Host, o Docker falhou na tentativa de `bind` da rede. O aprendizado técnico decorrente disso foi a flexibilidade do mapeamento de portas: pudemos redirecionar facilmente a porta Host (ex: 9000) para a porta interna do contêiner (8000) usando a flag `-p 9000:8000`, sem precisar alterar o código Python ou reconstruir o Dockerfile. Além disso, lidar com um erro inicial de serialização JSON reforçou a compreensão de como o volume preserva não apenas os dados estruturados, mas também os estados corrompidos, exigindo a limpeza do arquivo físico antes de prosseguir.
