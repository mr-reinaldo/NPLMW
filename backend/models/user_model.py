from sqlalchemy import String, Column, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from core.configs import settings


class UserModel(settings.DBBaseModel):
    """
    Classe UserModel para armazenar os dados do usuário.

    Args:
        settings (settings.DBBaseModel): Classe DBBaseModel do core.configs.

    """

    __tablename__ = "users"

    uuid = Column(
        String,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
    )
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devices = relationship(
        "DeviceModel",
        back_populates="owner",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="joined",
    )
