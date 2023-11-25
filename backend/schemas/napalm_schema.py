from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# Modelo de dados de dispositivo
class Device(BaseModel):
    hostname: str
    username: str
    password: str
    driver: str
    optional_args: Optional[dict] = None

# Modelo de dados de rota estática
class StaticRoute(BaseModel):
    route: str
    mask: str
    next_hop: str

# Modelo de requisição de rota estática 
class StaticRouteRequest(BaseModel):
    credentials: Device
    static_route: StaticRoute

# Modelo de dados 
class Data(BaseModel):
    hostname: str
    config: str
    diff: str
    timestamp: datetime

# Modelo de resposta de rota estática
class StaticRouteResponse(BaseModel):
    status: bool
    message: str
    data: Data

# Modelo de configuração de interface
class Interface(BaseModel):
    interface_name: str
    description: str
    ip_address: str
    netmask: str
    
# Modelo de requisição de interface
class InterfaceRequest(BaseModel):
    credentials: Device
    configurations: Interface

# Modelo de resposta de interface
class InterfaceResponse(BaseModel):
    status: bool
    message: str
    data: Data


class Information(BaseModel):
    vendor: str
    model: str
    serial_number: str
    os_version: str
    hostname: str
    fqdn: str
    uptime: float
    interfaces: List[Dict]
    arp_table: List[Dict]
    running_config: Dict
    
    
class InformationResponse(BaseModel):
    status: bool
    message: str
    data: Information
    timestamp: datetime

class PingData(BaseModel):

    # Quantidade de dispositivos de rede online
    devices_up: int

    # Quantidade de dispositivos de rede offline
    devices_down: int
    
class PingResponse(BaseModel):
    status: bool
    message: str
    data: PingData
    timestamp: datetime