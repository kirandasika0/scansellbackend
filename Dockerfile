FROM python:2.7-alpine
ENV PYTHONUNBUFFERED 1
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir src
WORKDIR src/
ADD . src/
EXPOSE 8000