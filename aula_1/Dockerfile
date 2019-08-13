FROM python:3.6

WORKDIR /app

RUN pip install flask && pip install pymongo && pip install jwt

COPY . /app

CMD [ "python", "ex_7.py"]