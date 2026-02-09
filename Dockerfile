FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m pip install -U pip \
  && python -m pip install -r requirements-dev.txt \
  && python -m pip install -e .

CMD ["bash", "devkit/check.sh"]
