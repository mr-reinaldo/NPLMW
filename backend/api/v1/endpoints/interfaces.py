from fastapi import APIRouter, HTTPException, status, Depends
from napalm import get_network_driver
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from schemas.napalm_schema import InterfaceRequest, InterfaceResponse
from core.deps import get_session, get_current_user


# Instanciando o router para as rotas estáticas
router = APIRouter()


# Carregando o template para configuração de rota estática
loader = FileSystemLoader("templates")
env = Environment(loader=loader)
template = env.get_template("interface.j2")


# Rota para configuração de interface
@router.post("/", response_model=InterfaceResponse, status_code=status.HTTP_201_CREATED)
async def interface(interface_request: InterfaceRequest, current_user = Depends(get_current_user)):
    # Obtendo os dados da requisição
    credentials = interface_request.credentials
    configurations = interface_request.configurations

    # Obtendo os dados do dispositivo
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

    # Configurando a interface
    try:
        config = template.render(
            interface_name=configurations.interface_name,
            ip_address=configurations.ip_address,
            netmask=configurations.netmask,
            description=configurations.description,
        )
        # Obtendo a data e hora atual
        now = datetime.now()
        
        print(config)
        
        # Aplicando a configuração
        device.load_merge_candidate(config=config)
        
        # Verificando as diferenças entre a configuração atual e a configuração que será aplicada
        diffs = device.compare_config()
        
        # Verificando se há diferenças entre as configurações
        if len(diffs) > 0:
            # Aplicando a configuração
            device.commit_config()
            status_req = True
            message = "Configuração aplicada com sucesso"
        else:
            status_req = False
            message = "Não há diferenças entre as configurações"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao configurar a interface devido a {e}",
        )
    finally:
        device.close()
        
    response =  InterfaceResponse(
        status=status_req,
        message=message,
        data={
            "hostname": credentials.hostname,
            "config": config,
            "diff": diffs,
            "timestamp": now,
        },
    )
    
    return response