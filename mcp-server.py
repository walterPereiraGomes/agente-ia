from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("backend-mcp")

KEYCLOAK_URL = "http://localhost:8085/realms/icmbio/protocol/openid-connect/token"
CLIENT_ID = "mcp"
CLIENT_SECRET = "sAQNod5ThBduavPHctljZDKKMEfty37d"

BACKEND_URL = "http://localhost:8080/gestao-perfis/api"

token_cache = {"access_token": None}

async def login_keycloak():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            KEYCLOAK_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )
        response.raise_for_status()
        token = response.json()["access_token"]
        token_cache["access_token"] = token
        return token

@mcp.tool()
async def listar_setores() -> list:
    """
    Retorna a lista de setores
    """

    if not token_cache["access_token"]:
        await login_keycloak()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/groups/setores",
            headers={
                "Authorization": f"Bearer {token_cache['access_token']}"
            }
        )
        print("resposta da api: {response}")
        response.raise_for_status()
        return response.json()
    
@mcp.tool()
async def listar_perfis() -> list:
    """
    Retorna a lista de setores
    """

    if not token_cache["access_token"]:
        await login_keycloak()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/groups/perfis",
            headers={
                "Authorization": f"Bearer {token_cache['access_token']}"
            }
        )
        print("resposta da api: {response}")
        response.raise_for_status()
        return response.json()
    
@mcp.tool()
async def listar_modulos() -> list:
    """
    Retorna a lista de setores
    """

    if not token_cache["access_token"]:
        await login_keycloak()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/clients",
            headers={
                "Authorization": f"Bearer {token_cache['access_token']}"
            }
        )
        print("resposta da api: {response}")
        response.raise_for_status()
        return response.json()
    
@mcp.tool()
async def listar_roles() -> list:
    """
    Retorna a lista de setores
    """

    if not token_cache["access_token"]:
        await login_keycloak()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/roles/all",
            headers={
                "Authorization": f"Bearer {token_cache['access_token']}"
            }
        )
        print("resposta da api: {response}")
        response.raise_for_status()
        return response.json()
    
@mcp.tool()
async def criar_perfil(
    name: str,
    roles: list[str],
    modules: list[dict]
) -> list:
    """
    Cria um novo perfil no sistema
    """

    if not token_cache["access_token"]:
        await login_keycloak()

    payload = {
        "name": name,
        "roles": roles,
        "modules": modules
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/groups",
            json=payload,
            headers={
                "Authorization": f"Bearer {token_cache['access_token']}"
            }
        )
        print("resposta da api: {response}")
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run()