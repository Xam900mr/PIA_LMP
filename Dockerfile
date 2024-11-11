FROM python:3.12-slim

WORKDIR /Aplicacion_Crud

RUN apt-get update && apt-get install -y netcat
 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["sh", "-c", "wait-for-it db:3306 -- python main.py"]