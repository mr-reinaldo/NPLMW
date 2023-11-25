from typing import Optional
from pydantic import BaseModel, validator

from pydantic.types import UUID4, PositiveInt
from re import match

from datetime import datetime


class DeviceSchema(BaseModel):

    """
    Classe DeviceSchema para validação de dados.

    Args:
        BaseModel (BaseModel): Classe BaseModel do Pydantic.

    """
    
    uuid: Optional[UUID4] = None
    hostname: str
    username: str
    password: str
    driver_name: str
    device_type: str
    device_name: str
    port: PositiveInt = 22
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    owner_uuid: Optional[UUID4] = None
    
    class Config:
        from_attributes = True

    
    # Validando porta.
    @validator("port")  # Decorador para o método de validação "validate_port".
    def validate_port(cls, port):
        """
        Método para validar porta.

        Args:
            port (int): Porta do dispositivo.

        Raises:
            ValueError: Porta inválida.

        Returns:
            int: Porta válida.

        """
        if (
            port < 1 or port > 65535
        ):  # Verifica se a porta está dentro do intervalo válido (1 a 65535).
            raise ValueError(
                "Porta inválida."
            )  # Se estiver fora do intervalo válido, lança uma exceção de valor inválido.
        return port  # Caso contrário, retorna a porta válida.

    # Validando hostname como endereço IPv4 ou IPv6 usando regex.
    @validator("hostname")
    def validate_hostname(cls, hostname):
        ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3}(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$"
        ipv6_pattern = r"^(?:(?:(?:[0-9a-fA-F]{1,4}):){6}(?:(?:25[0-5]|(?:2[0-4]|1?[0-9]){0,1}[0-9])\.){3}(?:25[0-5]|(?:2[0-4]|1?[0-9]){0,1}[0-9])|::(?:[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){0,6})?)$"

        if not match(ipv4_pattern, hostname) and not match(
            ipv6_pattern, hostname
        ):
            raise ValueError(
                "Hostname inválido. Deve ser um endereço IPv4 ou IPv6 válido."
            )
        return hostname