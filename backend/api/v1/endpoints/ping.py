from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from datetime import datetime
from core.deps import get_session, get_current_user
from subprocess import Popen, PIPE

from schemas.napalm_schema import PingResponse, PingData

class Ping:
    def __init__(self, ip_address: List[str]):
        self.list_ip: List[str] = ip_address
        self.devices_up: int = 0
        self.devices_down: int = 0
        
    def ping(self) -> PingData:
        for ip in self.list_ip:
            ping = Popen(["ping", "-c", "1","-W", "1", ip], stdout=PIPE, stderr=PIPE)
            
            output, error = ping.communicate()
            
            if ping.returncode == 0:
                self.devices_up += 1
            else:
                self.devices_down += 1
        
        return PingData(
            devices_up=self.devices_up,
            devices_down=self.devices_down
        )


router = APIRouter()

@router.post("/ping", response_model=PingResponse, status_code=status.HTTP_200_OK)
async def ping(ip_address: dict, current_user: str = Depends(get_current_user)):
    """
    Pinga os dispositivos de rede e retorna a quantidade de dispositivos online e offline.
    """
    
    # Dict to List
    ip_address = list(ip_address.values())
    
    ping = Ping(ip_address)
    
    try:
        result = ping.ping()
        
        return PingResponse(
            status=True,
            message="Ping realizado com sucesso!",
            data=result,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
