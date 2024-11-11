FROM python:3.12-slim

WORKDIR /Aplicacion_Crud
 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["sh", "-c", "wait-for-it db:3306 -- python main.py"]