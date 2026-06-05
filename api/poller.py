import asyncio
import httpx
from typing import Dict
from .models import Server

# Stockage en mémoire des serveurs
servers_db: Dict[str, Server] = {}

async def poll_server(server: Server):
    """Vérifie le statut d'un serveur spécifique."""
    url = f"{server.base_url()}/health"
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                server.status = "UP"
            else:
                server.status = "DEGRADED"
    except Exception:
        server.status = "DOWN"

async def run_poll_loop():
    """Boucle infinie pour vérifier tous les serveurs toutes les 10 secondes."""
    while True:
        if servers_db:
            tasks = [poll_server(server) for server in servers_db.values()]
            await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(10)
