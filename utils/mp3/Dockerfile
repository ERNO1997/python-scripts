FROM python:3.10.12-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir music

ENTRYPOINT ["python3", "mp3.py"]
CMD ["--help"]