FROM python:3.10-slim

COPY ./src /src
COPY requirements.txt /src

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

ENV TZ=Asia/Seoul
# CMD ["uvicorn", "main:app"]
# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "80"]
# CMD ["fastapi", "run", "src/main.py", "--port", "80"]

EXPOSE 24001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "24001"]
