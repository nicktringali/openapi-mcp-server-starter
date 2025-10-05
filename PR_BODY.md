Minimal stdio-only OpenAPI MCP Server starter wired to Petstore using the published PyPI package.

What’s included:
- Stdio-only run via uvx against Petstore v3 (make run)
- mcp.json for stdio with ENABLE_OPERATION_PROMPTS=true
- Makefile targets: run, tools-list, lint, typecheck, test, docker-build, docker-run
- requirements-dev.txt (ruff, mypy, pytest, pytest-cov)
- Smoke test using MCP Inspector CLI (opt-in; skips by default unless ENABLE_SMOKE_INSPECTOR=1)
- Dockerfile with "awslabs.openapi-mcp-server[all]"
- README quickstart and client usage notes

Notes:
- CI workflow intentionally omitted for now due to GitHub workflow permission scope; can be added once permissions are available.

Links:
- Link to Devin run: https://app.devin.ai/sessions/8ab66be5433e4d41b2b20e9d8d63d8c0
- Requested by: Nick Tringali (@nicktringali)
