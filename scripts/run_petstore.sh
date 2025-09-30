#!/usr/bin/env bash
set -euo pipefail
uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server \
  --api-name petstore \
  --api-url https://petstore3.swagger.io/api/v3 \
  --spec-url https://petstore3.swagger.io/api/v3/openapi.json \
  --log-level INFO
