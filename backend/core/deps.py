from typing import Generator, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status, Depends

from jose import jwt, JWTError

from pydantic import BaseModel

from core.configs import settings
from core.database import Session
from core.auth import oauth2_scheme

from models.user_model import UserModel


class TokenData(BaseModel):
    """
    Classe TokenData para armazenar os dados do token.

    Args:
        BaseModel (BaseModel): Classe BaseModel do pydantic.

    """

    username: Optional[str] = None


async def get_session() -> Generator:
    """
    Função para obter a sessão do banco de dados.

    Returns:
        Generator: Retorna a sessão do banco de dados.

    """

    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> UserModel:
    """
    Função para pegar o usuário logado no sistema.

    Args:
        db (Session, optional):
            Sessão do banco de dados. Defaults to Depends(get_session).
        token (str, optional):
            Token de acesso. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: Erro ao validar as credenciais.

    Returns:
        UserModel: Retorna o usuário logado no sistema.

    """

    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == str(token_data.username))
        result = await session.execute(query)

        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credentials_exception

        return user
