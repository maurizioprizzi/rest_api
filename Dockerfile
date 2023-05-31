# Define a imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o restante dos arquivos para o diretório de trabalho
COPY . .

# Define as variáveis de ambiente, se necessário
# ENV VARIAVEL=VALOR

# Expõe a porta que sua aplicação Flask está ouvindo
EXPOSE 5000

# Define o comando para executar a aplicação
CMD ["python", "app.py"]
