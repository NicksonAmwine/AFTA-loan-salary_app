FROM python:3.9-slim-buster
WORKDIR /app/streamlit_app
COPY ./streamlit_app /app/streamlit_app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]