# mcp-server-datahub

A [Model Context Protocol](https://modelcontextprotocol.io/) server implementation for [DataHub](https://datahubproject.io/).

## Features

Check out the [demo video](https://youtu.be/VXRvHIZ3Eww?t=1878), done in collaboration with the team at Block.

- Searching across all entity types and using arbitrary filters
- Fetching metadata for any entity
- Traversing the lineage graph, both upstream and downstream
- Listing SQL queries associated with a dataset
- `New` Now support for Docker Containers.
- `New` Support for http and sse.




## Usage

See instructions in the [DataHub MCP server docs](https://docs.datahub.com/docs/features/feature-guides/mcp).

### Docker Deployment 
#### Build
```cmd
docker build -t datahub-mcp:latest .
```

#### Run (inject your DataHub creds/URL)
```cmd
docker run --rm -p 8080:8080 \
  -e DATAHUB_GMS_URL="http://ip:port" \
  -e DATAHUB_GMS_TOKEN="your tocken here" \
  datahub-mcp:latest
```
## Json file to add to Cursor and other AI
```json
{
  "mcpServers": {
    "datahub": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```
## Developing

See [DEVELOPING.md](DEVELOPING.md).
