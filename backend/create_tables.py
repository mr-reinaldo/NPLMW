from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    """
    Função para criar tabelas no banco de dados.

    Explicação:
    Esta função é usada para criar as tabelas do banco de dados a partir dos modelos definidos.
    Os modelos são importados a partir dos módulos models.user_model e models.device_model.
    O objeto engine, que é uma instância do SQLAlchemy AsyncEngine, é usado para se comunicar com o banco de dados.
    A criação das tabelas é realizada através do método create_all do objeto metadata do DBBaseModel definido em core.configs.settings.
    Se as tabelas já existirem, elas serão apagadas antes de serem recriadas.

    """
    
    from models.user_model import UserModel
    from models.device_model import DeviceModel
    
    print("Criando tabelas...")
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        
    print("Tabelas criadas com sucesso!")
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
