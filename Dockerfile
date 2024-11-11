FROM python:3.12-slim

WORKDIR /Aplicacion_Crud
 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["python", "main.py", "--host=0.0.0.0", "--port=5000"]