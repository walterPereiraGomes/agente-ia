import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


def call_mcp_tool(nome_tool: str, argumentos: dict | None = None):
    """
    Executa uma tool no MCP Server e retorna o resultado.
    """

    if argumentos is None:
        argumentos = {}

    async def _call():
        server_params = StdioServerParameters(
            command="python",
            args=["mcp-server.py"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await session.call_tool(nome_tool, argumentos)

    return asyncio.run(_call())