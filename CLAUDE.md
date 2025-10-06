# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal stdio-only starter that demonstrates the AWS Labs OpenAPI MCP Server against the public Petstore API. The project wraps the published PyPI package `awslabs.openapi-mcp-server` and provides a simple way to test MCP server functionality without SSE/HTTP complexity.

**Key Links:**
- OpenAPI MCP Server docs: https://awslabs.github.io/mcp/servers/openapi-mcp-server/
- AWS MCP Servers monorepo: https://github.com/awslabs/mcp
- MCP Inspector: https://github.com/modelcontextprotocol/inspector

## Prerequisites

- Python 3.11+
- `uv` or `uvx` (preferred Python package runner)
- Node 18+ (for MCP Inspector CLI)
- Docker (optional, for containerized deployment)

## Common Commands

### Development Workflow
```bash
# Start the MCP server against Petstore API (stdio mode)
make run

# List available tools via MCP Inspector (non-interactive)
make tools-list

# Code quality checks
make lint        # ruff check .
make typecheck   # mypy .
make test        # pytest -q
```

### Docker Deployment
```bash
make docker-build    # Build container
make docker-run      # Run containerized server
```

### Manual Server Launch
```bash
# Direct launch with uvx
uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server \
  --api-name petstore \
  --api-url https://petstore3.swagger.io/api/v3 \
  --spec-url https://petstore3.swagger.io/api/v3/openapi.json \
  --log-level INFO
```

### Testing
```bash
# Run all tests
pytest -q

# Run smoke test with Inspector (requires opt-in)
ENABLE_SMOKE_INSPECTOR=1 pytest -q

# Run with coverage
pytest --cov
```

## Architecture

### Core Components

1. **mcp.json**: stdio configuration for MCP clients (Amazon Q, Claude Code, Cursor, MCP Inspector)
   - Launches server via `uvx` with Petstore API config
   - Environment variable: `ENABLE_OPERATION_PROMPTS=true`

2. **scripts/run_petstore.sh**: Bash wrapper for server launch
   - Sets `pipefail` for robust error handling
   - Calls `uvx` with Petstore parameters

3. **tests/test_smoke_inspector.py**: Integration test using MCP Inspector CLI
   - Skipped by default (opt-in with `ENABLE_SMOKE_INSPECTOR=1`)
   - Validates tools list endpoint returns expected Petstore operations
   - Requires Node/npx to be present

4. **Dockerfile**: Containerized deployment
   - Python 3.11-slim base
   - Installs `awslabs.openapi-mcp-server[all]`
   - CMD configured for Petstore API

### Key Patterns

- **Transport**: stdio-only (no SSE/HTTP endpoints)
- **Package management**: Uses `uvx` for ephemeral package execution (no local venv needed)
- **Testing**: Minimal smoke test that validates Inspector CLI integration
- **Configuration**: Centralized in `mcp.json` and `pyproject.toml`

## Code Quality Tools

### Ruff (linting)
- Target: Python 3.11
- Line length: 100
- Selected rules: E (errors), F (pyflakes), I (import sorting)
- Config: `pyproject.toml` [tool.ruff]

### Mypy (type checking)
- Python 3.11 target
- `ignore_missing_imports = true` (no dependency stubs required)
- `strict_optional = false`
- Config: `pyproject.toml` [tool.mypy]

### Pre-commit hooks
- ruff with `--fix` auto-correction
- black formatter (100 char line length)

### Pytest
- Minimum version: 7.0
- Default options: `-q` (quiet mode)
- Test paths: `tests/`

## Adding New API Targets

To adapt this starter for a different OpenAPI API:

1. Update `mcp.json`:
   - Change `--api-name` to your API identifier
   - Update `--api-url` to your API base URL
   - Update `--spec-url` to point to your OpenAPI spec JSON/YAML

2. Update `scripts/run_petstore.sh` with same parameters

3. Update `Dockerfile` CMD array with same parameters

4. Adjust tests in `tests/test_smoke_inspector.py`:
   - Modify assertion logic to match expected tool names from your API

## Important Notes

- This repo has no Python source code beyond tests—it's a wrapper/starter
- The actual MCP server logic lives in the upstream `awslabs.openapi-mcp-server` package
- No authentication is configured for Petstore (it's public)
- For authenticated APIs, see upstream docs on auth headers and environment variables
- The Inspector smoke test is opt-in to avoid network calls in CI by default
