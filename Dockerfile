FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
ARG VERSION
LABEL org.opencontainers.image.version=$VERSION
CMD ["tma", "status"]
