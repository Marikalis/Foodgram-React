FROM python:3.7-slim

WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev
RUN apt install -y gcc
RUN apt install nano && touch ~/.nanorc && echo include "/usr/share/nano/python.nanorc" >> ~/.nanorc

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
