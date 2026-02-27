import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp-server.py"],  # nome EXATO do seu arquivo
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("Tools disponíveis:")
            print(tools)

            resultado = await session.call_tool("listar_setores", {})
            print("Resultado:")
            print(resultado)

asyncio.run(main())