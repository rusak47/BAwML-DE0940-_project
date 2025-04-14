FROM python:3.13.2

WORKDIR app/

COPY ./app .
COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.baseUrlPath=/search"]
