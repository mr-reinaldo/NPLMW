from typing import Optional, List
from pydantic import BaseModel, EmailStr
from pydantic.types import UUID4

from datetime import datetime

from schemas.device_schema import DeviceSchema


class UserSchemaBase(BaseModel):

    """
    Classe UserSchemaBase para validação de dados.

    Args:
        BaseModel (BaseModel): Classe BaseModel do Pydantic.

    """
    
    uuid: Optional[UUID4] = None
    username: str
    email: EmailStr
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserSchemaCreate(UserSchemaBase):

    """
    Classe UserSchemaCreate para validação de dados.

    Args:
        UserSchemaBase (UserSchemaBase): Classe UserSchemaBase.

    """

    password: str


class UserSchemaUpdate(UserSchemaBase):
    
        """
        Classe UserSchemaUpdate para validação de dados.
    
        Args:
            UserSchemaBase (UserSchemaBase): Classe UserSchemaBase.
    
        """
        username: Optional[str] = None
        email: Optional[EmailStr] = None
        password: Optional[str] = None


class UserSchemaRelation(UserSchemaBase):

    """
    Classe UserSchemaRelation para validação de dados.

    Args:
        UserSchemaBase (UserSchemaBase): Classe UserSchemaBase.

    """

    devices: Optional[List[DeviceSchema]]