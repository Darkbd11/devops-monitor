import asyncio
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List

from .models import Server, ServerIn, ServerOut
from .metrics import get_system_metrics
from .auth import get_api_key
from .poller import run_poll_loop, servers_db, poll_server

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage de la boucle de polling au lancement
    task = asyncio.create_task(run_poll_loop())
    yield
    # Arrêt propre
    task.cancel()

app = FastAPI(
    title="DevOps Monitoring API",
    description="API de monitoring système par Darkbd11",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics")
def get_metrics():
    return get_system_metrics()

@app.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            metrics = get_system_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass

@app.post("/servers", response_model=ServerOut, status_code=201, dependencies=[Depends(get_api_key)])
def add_server(server_in: ServerIn):
    new_id = str(uuid.uuid4())
    new_server = Server(
        id=new_id,
        name=server_in.name,
        host=server_in.host,
        port=server_in.port
    )
    servers_db[new_id] = new_server
    return new_server

@app.get("/servers", response_model=List[ServerOut])
def list_servers():
    return list(servers_db.values())

@app.delete("/servers/{server_id}", status_code=204, dependencies=[Depends(get_api_key)])
def delete_server(server_id: str):
    if server_id not in servers_db:
        raise HTTPException(status_code=404, detail="Serveur introuvable")
    del servers_db[server_id]
    return None

@app.post("/servers/{server_id}/check")
async def check_server_now(server_id: str):
    if server_id not in servers_db:
        raise HTTPException(status_code=404, detail="Serveur introuvable")
    server = servers_db[server_id]
    await poll_server(server)
    return {"status": server.status}
