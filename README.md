# OpenAPI MCP Server Starter (Petstore, stdio-only)

A minimal starter that launches the AWS Labs OpenAPI MCP Server against the public Petstore API via the published PyPI package `awslabs.openapi-mcp-server`. This repo is stdio-only (no SSE/HTTP). Quick to clone and verify in under 5 minutes.

Links:
- OpenAPI MCP Server docs: https://awslabs.github.io/mcp/servers/openapi-mcp-server/
- AWS MCP Servers monorepo: https://github.com/awslabs/mcp
- MCP Inspector: https://github.com/modelcontextprotocol/inspector

## Prerequisites
- Python 3.11+ and uv (preferred) or pip
- Node 18+ for MCP Inspector CLI (optional but recommended)
- Docker (optional)

## Quickstart
Clone and run:
- make run         # start server (stdio) against Petstore
- make tools-list  # list tools via MCP Inspector CLI (non-interactive)

Verification:
- make lint
- make typecheck
- make test

## mcp.json (stdio)
Use this with MCP clients (Amazon Q, Claude Code, Cursor, MCP Inspector):
See mcp.json in this repo for a ready-to-use stdio config that runs the Petstore server via uvx.

## Commands
- make run
- make tools-list
- make lint
- make typecheck
- make test
- make docker-build && make docker-run

## Interactive with MCP Inspector
- npx @modelcontextprotocol/inspector
- Choose “Launch from command” and paste:
  uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server \
    --api-name petstore \
    --api-url https://petstore3.swagger.io/api/v3 \
    --spec-url https://petstore3.swagger.io/api/v3/openapi.json \
    --log-level INFO

## Notes
- This starter is stdio-only to avoid SSE/HTTP complexity. See upstream docs for other transports.
- Petstore is public; no auth required.

## License
Apache-2.0 (follow upstream).
