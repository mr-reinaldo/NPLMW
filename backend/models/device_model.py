from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from core.configs import settings


class DeviceModel(settings.DBBaseModel):
    """
    Classe DeviceModel para armazenar os dados do dispositivo.

    Args:
        settings (settings.DBBaseModel): Classe DBBaseModel do core.configs.

    """

    __tablename__ = "devices"

    uuid = Column(
        String,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
    )
    hostname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    driver_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    device_name = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    owner_uuid = Column(String, ForeignKey("users.uuid"))
    
    owner = relationship("UserModel", back_populates="devices", lazy="joined")