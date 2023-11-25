# Importando tipos de dados.
from typing import List
# Importando módulos do FastAPI.
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
)
from fastapi.responses import JSONResponse, Response
# Importando módulos do SQLAlchemy.
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
# Importando módulos core da aplicação.
from core.deps import (
    get_session,
    get_current_user,
)
# Importando modelo de dados (DeviceModel).
from models.device_model import (
    DeviceModel,
)
# Importando modelo de dados (UserModel).
from models.user_model import (
    UserModel,
)
# Importando esquema de dados (schema) para validação.
from schemas.device_schema import (
    DeviceSchema,
)

# Criando roteador FastAPI.
router = APIRouter()



# Definindo rota para criação de dispositivos.
@router.post(
    "/", response_model=DeviceSchema, status_code=status.HTTP_201_CREATED
)
async def create_device(
    device: DeviceSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> DeviceModel:
    """
    Definindo rota para criação de dispositivos.

    Args:
        device (DeviceModel): Modelo de dados do dispositivo.
        current_user (UserModel): Modelo de dados do usuário logado.

    Returns:
        DeviceModel: Retorna o dispositivo criado.

    """

    new_device: DeviceModel = DeviceModel(
        hostname=device.hostname,
        username=device.username,
        password=device.password,
        driver_name=device.driver_name,
        device_type=device.device_type,
        device_name=device.device_name,
        port=device.port,
        owner_uuid=current_user.uuid,
    )

    try:
        async with db as session:
            query = select(DeviceModel).filter(
                DeviceModel.hostname == device.hostname
            )
            result = await session.execute(query)
            device: DeviceModel = result.scalars().unique().one_or_none()

            if device:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Um dispositivo com este hostname já existe.",
                )
            else:
                session.add(new_device)
                await session.commit()

                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={
                        "message": "Dispositivo criado com sucesso.",
                    },
                )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar dispositivo.",
        )


# Definindo rota para listagem de dispositivos (se o usuário estiver autenticado).
@router.get(
    "/", response_model=List[DeviceSchema], status_code=status.HTTP_200_OK
)
async def list_devices(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> List[DeviceModel]:
    """
    Definindo rota para listagem de dispositivos (se o usuário estiver autenticado).

    Args:
        current_user (UserModel): Modelo de dados do usuário logado.

    Returns:
        List[DeviceModel]: Retorna uma lista de dispositivos.

    """

    try:
        async with db as session:
            query = select(DeviceModel)
            result = await session.execute(query)
            devices: List[DeviceModel] = result.scalars().unique().all()

            if not devices:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nenhum dispositivo encontrado.",
                )
            else:
                return devices

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao listar dispositivos.",
        )


# Definindo rota para listagem de dispositivos por UUID (se o usuário estiver autenticado).
@router.get(
    "/{uuid}", response_model=DeviceSchema, status_code=status.HTTP_200_OK
)
async def list_device_by_uuid(
    uuid: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> DeviceModel:
    """
    Definindo rota para listagem de dispositivos por UUID (se o usuário estiver autenticado).

    Args:
        uuid (str): UUID do dispositivo.
        current_user (UserModel): Modelo de dados do usuário logado.

    Returns:
        DeviceModel: Retorna o dispositivo.

    """

    try:
        async with db as session:
            query = select(DeviceModel).filter(DeviceModel.uuid == uuid)
            result = await session.execute(query)
            device: DeviceModel = result.scalars().unique().one_or_none()

            if not device:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dispositivo não encontrado.",
                )
            else:
                return device

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao listar dispositivo.",
        )


# Definindo rota para atualização de dispositivos por UUID (se o usuário estiver autenticado).
@router.put(
    "/{uuid}",
    response_model=DeviceSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_device_by_uuid(
    uuid: str,
    device: DeviceSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> DeviceModel:
    """
    Definindo rota para atualização de dispositivos por UUID (se o usuário estiver autenticado).

    Args:
        uuid (str): UUID do dispositivo.
        device (DeviceModel): Modelo de dados do dispositivo.
        current_user (UserModel): Modelo de dados do usuário logado.

    Returns:
        DeviceModel: Retorna o dispositivo atualizado.

    """

    try:
        async with db as session:
            query = select(DeviceModel).filter(DeviceModel.uuid == uuid)
            result = await session.execute(query)
            device_db: DeviceModel = result.scalars().unique().one_or_none()

            if not device_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dispositivo não encontrado.",
                )

            else:
                if current_user.uuid != device_db.owner_uuid:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Você não tem permissão para atualizar este dispositivo.",
                    )

                else:
                    if device.hostname:
                        device_db.hostname = device.hostname

                    if device.username:
                        device_db.username = device.username

                    if device.password:
                        device_db.password = device.password

                    if device.device_type:
                        device_db.device_type = device.device_type

                    if device.driver_name:
                        device_db.driver_name = device.driver_name
                        
                    if device.device_name:
                        device_db.device_name = device.device_name

                    if device.port:
                        device_db.port = device.port

                    await session.commit()

                    return JSONResponse(
                        status_code=status.HTTP_202_ACCEPTED,
                        content={
                            "message": "Dispositivo atualizado com sucesso.",
                        },
                    )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar dispositivo.",
        )


# Definindo rota para remoção de dispositivos por UUID (se o usuário estiver autenticado).
@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_by_uuid(
    uuid: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> Response:
    """
    Definindo rota para remoção de dispositivos por UUID (se o usuário estiver autenticado).

    Args:
        uuid (str): UUID do dispositivo.
        current_user (UserModel): Modelo de dados do usuário logado.

    Returns:
        Response: Retorna uma resposta vazia.

    """

    try:
        async with db as session:
            query = select(DeviceModel).filter(DeviceModel.uuid == uuid)
            result = await session.execute(query)
            device: DeviceModel = result.scalars().unique().one_or_none()

            if not device:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dispositivo não encontrado.",
                )

            else:
                if current_user.uuid != device.owner_uuid:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Você não tem permissão para remover este dispositivo.",
                    )

                else:
                    await session.delete(device)
                    await session.commit()

                    return JSONResponse(
                        status_code=status.HTTP_204_NO_CONTENT,
                        content={
                            "message": "Dispositivo removido com sucesso.",
                        },
                    )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao remover dispositivo.",
        )