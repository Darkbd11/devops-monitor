from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional

@dataclass
class Server:
    id: str
    name: str
    host: str
    port: int
    status: str = "UNKNOWN" # UP, DOWN, DEGRADED, UNKNOWN

    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

class ServerIn(BaseModel):
    name: str
    host: str
    port: int = Field(..., ge=1, le=65535)

class ServerOut(BaseModel):
    id: str
    name: str
    host: str
    port: int
    status: str
