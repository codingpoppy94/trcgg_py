# FROM python:3.10.0
FROM arm64v8/python:3

COPY ./src /src
COPY requirements.txt /src

WORKDIR /src

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV TZ=Asia/Seoul
# CMD ["uvicorn", "main:app"]
# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "80"]
# CMD ["fastapi", "run", "src/main.py", "--port", "80"]

EXPOSE 24002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "24002"]