# testMCP
make MCP server for Test by modelcontextprotocol & fastmcp

## ModelContextProtocol
### SetUp
```
npm install

npm run build
```

### Inspector
```
npx @modelcontextprotocol/inspector node build/index.js
```

## FastMCP
### SetUp
```
python3 -m venv .venv
source .venv/bin/activate

pip install fastmcp
```
### Inspector
```
npx @modelcontextprotocol/inspector python3 fastMCP/server.py
```