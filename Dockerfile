# I'm not sure what it is right
FROM python:2.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt