from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from napalm import get_network_driver
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from core.deps import get_session, get_current_user
from schemas.napalm_schema import Device, InformationResponse

router = APIRouter()


def mount_data(device):
    facts = device.get_facts()
    interfaces = device.get_interfaces()
    interfaces_ip = device.get_interfaces_ip()
    running_config = device.get_config(retrieve="running", sanitized=True)
    arp_table = device.get_arp_table()

    information = {
            "vendor": facts.get("vendor", ""),
            "model": facts.get("model", ""),
            "serial_number": facts.get("serial_number", ""),
            "os_version": facts.get("os_version", ""),
            "hostname": facts.get("hostname", ""),
            "fqdn": facts.get("fqdn", ""),
            "uptime": facts.get("uptime", ""),
            "interfaces": [
                {
                    "name": interface,
                    "description": interfaces[interface].get("description", ""),
                    "is_enabled": interfaces[interface].get("is_enabled", ""),
                    "is_up": interfaces[interface].get("is_up", ""),
                    "mac_address": interfaces[interface].get("mac_address", ""),
                    "last_flapped": interfaces[interface].get("last_flapped", ""),
                    "speed": interfaces[interface].get("speed", ""),
                    "mtu": interfaces[interface].get("mtu", ""),
                    "ipv4": interfaces_ip.get(interface, {}).get("ipv4", {}),
                    "ipv6": interfaces_ip.get(interface, {}).get("ipv6", {}),
                }
                for interface in interfaces
            ],
            "arp_table": arp_table,
            "running_config": running_config,
        }
    return information

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InformationResponse)
async def facts(device: Device, current_user = Depends(get_current_user)):
    driver = get_network_driver(device.driver)
    device = driver(
        device.hostname,
        device.username,
        device.password,
        optional_args=device.optional_args,
    )
    try:
        device.open()
        
        data = mount_data(device)  
        device.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao obter informações do dispositivo {device.hostname}",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": True,
            "message": f"Informações do dispositivo {device.hostname} obtidas com sucesso",
            "data": data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )