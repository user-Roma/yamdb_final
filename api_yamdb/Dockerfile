FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
LABEL author='User_Roma' version=01