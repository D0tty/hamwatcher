from alpine:latest

ENV DISPLAY=:99

RUN apk add --no-cache \
  chromium-chromedriver \
  poetry \
  py3-pip \
  python3
RUN pip install selenium

RUN mkdir /app
WORKDIR /app

COPY app.py .
COPY config.py .
COPY last.txt .
COPY pyproject.toml .

RUN poetry install

CMD ["poetry", "run", "python", "app.py"]