FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir "awslabs.openapi-mcp-server[all]"
CMD ["awslabs.openapi-mcp-server","--api-name","petstore","--api-url","https://petstore3.swagger.io/api/v3","--spec-url","https://petstore3.swagger.io/api/v3/openapi.json","--log-level","INFO"]
