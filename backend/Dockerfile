FROM python:3.10-slim
LABEL author="danpautoff@yandex.ru"
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update -y
RUN apt-get install libpq-dev -y
RUN apt-get install gcc -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY foodgram/ ./
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]