.PHONY: run tools-list lint typecheck test docker-build docker-run

run:
	./scripts/run_petstore.sh

tools-list:
	npx --yes @modelcontextprotocol/inspector --cli -- uvx --from awslabs.openapi-mcp-server@latest awslabs.openapi-mcp-server --api-name petstore --api-url https://petstore3.swagger.io/api/v3 --spec-url https://petstore3.swagger.io/api/v3/openapi.json --method tools/list

lint:
	ruff check .

typecheck:
	mypy .

test:
	pytest -q

docker-build:
	docker build -t openapi-mcp-server:latest .

docker-run:
	docker run --rm -it openapi-mcp-server:latest
