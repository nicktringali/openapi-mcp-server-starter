# OpenAPI MCP Server Starter (Petstore, stdio-only)

A minimal starter that launches the AWS Labs OpenAPI MCP Server against the public Petstore API via the published PyPI package `awslabs.openapi-mcp-server`. This repo is stdio-only (no SSE/HTTP). Quick to clone and verify in under 5 minutes.

**What is this?** This server automatically converts any OpenAPI specification into MCP tools that AI assistants (Claude, ChatGPT, etc.) can use to interact with APIs. No manual tool definitions required—just point it at an OpenAPI spec and the AI gets instant access to all endpoints with proper descriptions and parameter validation.

Links:
- OpenAPI MCP Server docs: https://awslabs.github.io/mcp/servers/openapi-mcp-server/
- AWS MCP Servers monorepo: https://github.com/awslabs/mcp
- MCP Inspector: https://github.com/modelcontextprotocol/inspector

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Using with MCP Clients](#using-with-mcp-clients)
- [What You Can Do with the Petstore API](#what-you-can-do-with-the-petstore-api)
- [Advanced Features](#advanced-features)
- [Development Commands](#development-commands)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Python 3.11+ and uv (preferred) or pip
- Node 18+ for MCP Inspector CLI (optional but recommended)
- Docker (optional)

## Quickstart
Clone and run:
```bash
make run         # start server (stdio) against Petstore
make tools-list  # list tools via MCP Inspector CLI (non-interactive)
```

Verification:
```bash
make lint        # ruff linting
make typecheck   # mypy type checking
make test        # pytest suite
```

## Using with MCP Clients

This server works with any MCP-compatible client. The included `mcp.json` provides a ready-to-use configuration.

### Claude Desktop

1. **Open Claude Desktop settings:**
   - Click **Settings** → **Developer** → **Edit Config**
   - Or manually edit: `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)

2. **Add this server configuration:**
```json
{
  "mcpServers": {
    "petstore": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "awslabs.openapi-mcp-server@latest",
        "awslabs.openapi-mcp-server",
        "--api-name",
        "petstore",
        "--api-url",
        "https://petstore3.swagger.io/api/v3",
        "--spec-url",
        "https://petstore3.swagger.io/api/v3/openapi.json",
        "--log-level",
        "INFO"
      ],
      "env": {
        "ENABLE_OPERATION_PROMPTS": "true"
      }
    }
  }
}
```

3. **Restart Claude Desktop** (required for changes to take effect)

4. **Verify it's working:**
   - Start a new conversation
   - Type: "List all available pets in the store"
   - Claude should use the MCP tools to call the Petstore API

### Claude Code CLI

The `mcp.json` in this repo is already configured for Claude Code:

```bash
# Copy mcp.json to your Claude Code config directory
cp mcp.json ~/.config/claude-code/mcp.json

# Or add it to your project-specific .claude/mcp.json
```

### Cursor

Cursor uses the same format but requires manual configuration through its UI:

1. Open **Settings** → **MCP Servers**
2. Add a new server with the command: `uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server --api-name petstore --api-url https://petstore3.swagger.io/api/v3 --spec-url https://petstore3.swagger.io/api/v3/openapi.json`

**Note:** Cursor doesn't support `.mcpb` bundles or batch import yet, so servers must be added individually.

### Testing with MCP Inspector

The MCP Inspector provides a web UI for testing your server:

```bash
npx @modelcontextprotocol/inspector
```

Then:
1. Choose **"Launch from command"**
2. Paste the uvx command:
```bash
uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server \
  --api-name petstore \
  --api-url https://petstore3.swagger.io/api/v3 \
  --spec-url https://petstore3.swagger.io/api/v3/openapi.json \
  --log-level INFO
```
3. Inspector opens at `http://localhost:6274`
4. Test tools like `addPet`, `findPetsByStatus`, etc.

## What You Can Do with the Petstore API

Once connected, AI assistants can perform these operations:

### Pet Management
- **Add new pets** to the store with details (name, category, tags, status)
- **Update existing pets** by ID
- **Search pets by status** (available, pending, sold)
- **Search pets by tags** for categorization
- **Get pet details** by ID
- **Delete pets** from the store
- **Upload pet images** with metadata

### Store Operations
- **Check inventory** - Get pet counts by status
- **Place orders** - Create purchase orders for pets
- **Retrieve orders** - Get order details by ID
- **Cancel orders** - Delete purchase orders

### User Management
- **Create user accounts**
- **Login/logout** - Authenticate users
- **Update user profiles**
- **Delete user accounts**
- **Batch user creation** - Create multiple users at once

### Example Prompts to Try

Once configured in Claude Desktop or Claude Code, try these:

```
"Show me all available pets in the store"

"Add a new dog named Max with the category 'Dogs' and tag 'friendly'"

"What's the current inventory status?"

"Place an order for pet ID 1"

"Create a user account for john_doe with email john@example.com"
```

The AI will automatically:
1. Determine which API endpoint(s) to call
2. Format the request with proper parameters
3. Handle authentication (if configured)
4. Parse and explain the response

## Advanced Features

### ENABLE_OPERATION_PROMPTS

This server has `ENABLE_OPERATION_PROMPTS` set to `"true"` in the environment. This feature:
- **Generates natural language prompts** for each API operation
- **Helps LLMs understand** what each endpoint does without reading raw OpenAPI specs
- **Reduces token usage** by 70-75% through concise, contextualized descriptions
- **Improves accuracy** by providing clear operation semantics

### Using uvx (No Installation Required)

This starter uses `uvx`, which:
- **Runs Python tools without installing them** - like `npx` for Node.js
- **Creates temporary isolated environments** - no dependency conflicts
- **Caches installations** - subsequent runs take milliseconds
- **Stays up-to-date** - always uses `@latest` version

Benefits:
- No need to manage virtual environments
- No bloated `node_modules` equivalent
- Works immediately after cloning the repo

### Token Usage Optimization

The OpenAPI MCP Server is designed for efficiency:
- Concise tool descriptions reduce prompt tokens
- Structured parameter validation prevents invalid requests
- Intelligent route mapping minimizes API calls
- Response parsing extracts only relevant data

## Development Commands

```bash
# Run the server locally
make run

# List available tools (requires Node/npx)
make tools-list

# Code quality
make lint           # Run ruff linter
make typecheck      # Run mypy type checker
make test           # Run pytest tests

# Docker deployment
make docker-build   # Build container image
make docker-run     # Run containerized server
```

### Running Tests

```bash
# Run all tests (smoke test skipped by default)
pytest -q

# Run smoke test with MCP Inspector (requires Node)
ENABLE_SMOKE_INSPECTOR=1 pytest -q

# Run with coverage
pytest --cov
```

## Adapting to Your Own API

To use this starter with your own OpenAPI API:

1. **Update `mcp.json`:**
```json
{
  "mcpServers": {
    "your-api-name": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "awslabs.openapi-mcp-server@latest",
        "awslabs.openapi-mcp-server",
        "--api-name", "your-api",
        "--api-url", "https://api.example.com/v1",
        "--spec-url", "https://api.example.com/openapi.json",
        "--log-level", "INFO"
      ],
      "env": {
        "ENABLE_OPERATION_PROMPTS": "true",
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. **Add authentication if needed:**
```bash
# Bearer token
--auth-type bearer --auth-token "your-token"

# API key in header
--auth-type api-key --auth-header-name "X-API-Key" --auth-token "your-key"

# Basic auth
--auth-type basic --auth-username "user" --auth-password "pass"
```

3. **Update `scripts/run_petstore.sh` and `Dockerfile`** with your API parameters

4. **Test locally** before deploying

## Troubleshooting

### "Command not found: uvx"

Install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

### "MCP Inspector tools-list fails"

This is a known compatibility issue with Node v24. The core server works fine—Inspector is just for testing. Workarounds:
- Use MCP Inspector interactive mode (`npx @modelcontextprotocol/inspector`)
- Downgrade to Node v18 or v20
- Skip the Inspector test (it's optional)

### "No tools showing up in Claude Desktop"

1. **Check the config file location** - Make sure you edited the right file
2. **Restart Claude Desktop** - Configuration changes require a restart
3. **Check logs** - Look at Claude Desktop's logs for error messages
4. **Test with Inspector** - Verify the server works outside of Claude Desktop

### "API calls failing with authentication errors"

- **For Petstore:** No auth required (it's public)
- **For your API:** Add authentication to the `env` section or use `--auth-*` flags
- Check that your API key/token has proper permissions

### Transport Compatibility Issues

**stdio (this repo):**
- ✅ Works with: Claude Desktop, Claude Code, Cursor
- ✅ Simple configuration
- ✅ No network setup required

**SSE/HTTP:**
- ⚠️ Claude Desktop doesn't support remote SSE endpoints
- ✅ Works with Cursor
- Requires proxy for Claude Desktop

## Notes
- This starter is stdio-only to avoid SSE/HTTP complexity. See upstream docs for other transports.
- Petstore is public; no auth required.
- The server automatically handles OpenAPI 3.0 and 3.1 specifications.
- Supports JSON and YAML OpenAPI specs (install with `[yaml]` extra for YAML).

## Security Considerations

When deploying MCP servers:

1. **Use authentication** for production APIs (Petstore is public/demo only)
2. **Don't expose servers** directly to the internet without auth
3. **Validate OpenAPI specs** before using them (malicious specs could expose unintended data)
4. **Use environment variables** for secrets, never hardcode in config files
5. **Keep uv/uvx updated** to get security patches
6. **Review API permissions** - MCP servers have full access to the APIs they're configured for

## Real-World Use Cases

This pattern is used in production for:

- **Database management** (SQL query generation, schema exploration)
- **Cloud infrastructure** (AWS, Azure, GCP API access)
- **SaaS integrations** (Slack, GitHub, Jira, etc.)
- **Internal tools** (Company APIs, microservices)
- **Competitive analysis** (Price monitoring, market data)
- **Content management** (CMS APIs, media libraries)

The OpenAPI → MCP bridge reduces integration time from weeks to hours by eliminating manual tool definitions.

## License
Apache-2.0 (follow upstream).
