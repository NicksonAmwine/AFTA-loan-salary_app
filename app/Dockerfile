FROM python:3.9-slim-buster
WORKDIR /app/app
COPY ./app /app/app
RUN pip install -r requirements.txt 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]