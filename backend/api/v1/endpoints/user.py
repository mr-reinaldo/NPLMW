from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.deps import get_session, get_current_user
from core.auth import authenticate, generate_access_token
from core.security import generate_password_hash

from models.user_model import UserModel

from schemas.user_schema import (
    UserSchemaBase,
    UserSchemaCreate,
    UserSchemaUpdate,
    UserSchemaRelation,
)

router = APIRouter()


# Definindo rota para verificar o usuário logado.
@router.get("/me", response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def get_me(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """Retorna o usuário logado.

    Args:
        current_user (UserModel, optional): Usuário logado. Defaults to Depends(get_current_user).

    Returns:
        UserModel: Usuário logado.

    """

    return current_user


# Definindo rota para criar novos usuários.
@router.post(
    "/signup", response_model=UserSchemaBase, status_code=status.HTTP_201_CREATED
)
async def signup(
    user: UserSchemaCreate, db: AsyncSession = Depends(get_session)
) -> UserModel:
    """Cria um novo usuário.

    Args:
        user (UserSchemaCreate): Dados do usuário.
        db (AsyncSession, optional): Sessão do banco de dados. Defaults to Depends(get_session).

    Raises:
        HTTPException: E-mail já cadastrado.
        HTTPException: Erro ao criar o usuário.

    Returns:
        JSONResponse: Resposta de sucesso.

    """

    new_user: UserModel = UserModel(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
    )

    try:
        async with db as session:
            query = select(UserModel).filter(UserModel.email == new_user.email)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="E-mail já cadastrado.",
                )

            session.add(new_user)
            await session.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Usuário criado com sucesso."},
            )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o usuário.",
        )


# Definindo rota para listar todos os usuários (usuário deve estar autenticado).
@router.get("/", response_model=List[UserSchemaBase], status_code=status.HTTP_200_OK)
async def get_users(
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> List[UserModel]:
    """Lista todos os usuários.

    Args:
        db (AsyncSession, optional): Sessão do banco de dados. Defaults to Depends(get_session).
        current_user (UserModel, optional): Usuário logado. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Nenhum usuário encontrado.

    Returns:
        List[UserSchemaBase]: Lista de usuários.

    """
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().unique().all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum usuário encontrado.",
            )

        return users


# Definindo rota para listar usuário por UUID (usuário deve estar autenticado).
@router.get("/{uuid}", response_model=UserSchemaRelation, status_code=status.HTTP_200_OK)
async def get_user_by_uuid(
    uuid: str,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Retorna um usuário por UUID.

    Args:
        uuid (str): UUID do usuário.
        db (AsyncSession, optional): Sessão do banco de dados. Defaults to Depends(get_session).
        current_user (UserModel, optional): Usuário logado. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Usuário não encontrado.

    Returns:
        UserSchemaRelational: Usuário.

    """
    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == uuid)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )

        return user


# Definindo rota para atualizar usuário por UUID (usuário deve estar autenticado).
@router.put(
    "/{uuid}",
    response_model=UserSchemaBase,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user_by_uuid(
    uuid: str,
    user: UserSchemaUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Atualiza um usuário por UUID.

    Args:
        uuid (str): UUID do usuário.
        user (UserSchemaUpdate): Dados do usuário.
        db (AsyncSession, optional): Sessão do banco de dados. Defaults to Depends(get_session).
        current_user (UserModel, optional): Usuário logado. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Usuário não encontrado.

    Returns:
        UserSchemaBase: Usuário atualizado.

    """
    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == uuid)
        result = await session.execute(query)
        user_db: UserModel = result.scalars().unique().one_or_none()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )

        if user.username:
            user_db.username = user.username
        if user.email:
            user_db.email = user.email
        if user.password:
            user_db.password = generate_password_hash(user.password)

        await session.commit()

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "detail": "Usuário atualizado com sucesso.",
                "user_uuid": str(user_db.uuid),
            },
        )


# Rota para deletar um usuário por UUID (usuário deve estar autenticado).
@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uuid(
    uuid: str,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Deleta um usuário por UUID.

    Args:
        uuid (str): UUID do usuário.
        db (AsyncSession, optional): Sessão do banco de dados. Defaults to Depends(get_session).
        current_user (UserModel, optional): Usuário logado. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Usuário não encontrado.

    Returns:
        Response: Resposta de sucesso.

    """
    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == uuid)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )

        await session.delete(user)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


# Definindo rota de autenticação.
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
        )

    return JSONResponse(
        content={
            "access_token": generate_access_token(sub=user.uuid),
            "token_type": "Bearer",
        },
        status_code=status.HTTP_200_OK,
    )
