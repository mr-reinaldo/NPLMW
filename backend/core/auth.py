from typing import Optional

from pytz import timezone
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import EmailStr

from core.configs import settings
from core.security import verify_password


from models.user_model import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")


async def authenticate( email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    """
    Função asincrona para autenticação do usuário.

    Args:
        email (EmailStr): Email do usuário.
        password (str): Senha do usuário.
        db (AsyncSession): Sessão do banco de dados.

    Returns:
        Optional[UserModel]: Retorna o usuário autenticado.

    """
    
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        

        return user


def _create_token(type_token:str, lifetime: timedelta, sub: str) -> str:
    """
    Função privada para gerar o token de acesso.

    Link para mais informações sobre o JWT:
    https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3

    Args:
        type_token (str): Tipo de token.
        lifetime (timedelta): Tempo de vida do token.
        sub (str): Identificador do usuário.

    Returns:
        str: Token de acesso.

    """
    
    sp = timezone(settings.TIMEZONE)
    
    expire = datetime.now(tz=sp) + lifetime
    
    payload = {
        "type": type_token,
        "exp": expire,
        "iat": datetime.now(tz=sp),
        "sub": str(sub),
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_access_token(sub: str) -> str:
    """
    Função para gerar o token de acesso.

    Link para mais informações sobre o JWT:
    https://jwt.io

    Args:
        sub (str): Identificador do usuário.

    Returns:
        str: Token de acesso.

    """
    
    return _create_token(
        type_token="access_token",
        lifetime=timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        sub=sub,
    )