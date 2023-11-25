from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from napalm import get_network_driver
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from schemas.napalm_schema import StaticRouteRequest, StaticRouteResponse

from core.deps import get_session, get_current_user

# Instanciando o router para as rotas estáticas
router = APIRouter()


# Carregando o template para configuração de rota estática
loader = FileSystemLoader('templates')
env = Environment(loader=loader)
template = env.get_template('static_route.j2')


@router.post('/', response_model=StaticRouteResponse, status_code=status.HTTP_201_CREATED)
async def static_route(static_route_request: StaticRouteRequest, current_user = Depends(get_current_user)):
    """Rota para configuração de rota estática"""
    # Obtendo as credenciais para conexão com o dispositivo
    credentials = static_route_request.credentials

    # Obtendo os dados da rota estática
    static_route = static_route_request.static_route

    # Obtendo o driver para conexão com o dispositivo
    driver = get_network_driver(credentials.driver)
    
    # Conectando ao dispositivo
    try:
        device = driver(
            credentials.hostname,
            credentials.username,
            credentials.password,
            optional_args=credentials.optional_args,
        )
        device.open()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao conectar ao dispositivo devido a {e}",
        )

    # Montando a configuração
    try:
        config = template.render(
            route=static_route.route, 
            mask=static_route.mask, 
            next_hop=static_route.next_hop
        )
        
        # Obtendo a data e hora atual
        now = datetime.now()
        # Aplicando a configuração
        device.load_merge_candidate(config=config)
        
        # Verificando as diferenças entre a configuração atual e a configuração que será aplicada
        diffs = device.compare_config()
    
        # Verificando se há diferenças
        if len(diffs) > 0:
            # Aplicando a configuração
            device.commit_config()
            status_req = True
            message = "Rotas estáticas configuradas com sucesso!"
        else:
            status_req = False
            message = "Não há diferenças entre a configuração atual e a configuração que será aplicada!"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao configurar rota estática devido a {e}",
        )
        
    # Obtendo a data e hora atual
    now = datetime.now()
    
    # Montando a resposta
    response = StaticRouteResponse(
        status=status_req,
        message=message,
        data={
            "hostname": credentials.hostname,
            "config": config,
            "diff": diffs,
            "timestamp": now,
        },
    )
    
    # Retornando a resposta
    return response