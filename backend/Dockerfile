FROM python:3.10-slim
LABEL author="danpautoff@yandex.ru"
WORKDIR /app
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY foodgram/ ./
CMD python3 manage.py migrate ; python3 manage.py collectstatic --no-input ; gunicorn foodgram.wsgi:application --bind 0:8000