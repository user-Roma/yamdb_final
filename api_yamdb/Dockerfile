FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "app.api_yamdb.wsgi:application", "--bind", "0:8000"]
LABEL author='User_Roma' version=01