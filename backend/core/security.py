from passlib.context import CryptContext


CRYPTO_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str , hashed_password: str) -> bool:
    """
    Função para verificar a senha.

    Args:
        plain_password (str): Senha em texto plano.
        hashed_password (str): Senha criptografada.

    Returns:
        bool: Retorna True se a senha estiver correta, caso contrário
        retorna False.

    """
    
    return CRYPTO_CONTEXT.verify(plain_password, hashed_password)



def generate_password_hash(password: str) -> str:
    """
    Função para gerar o hash da senha.

    Args:
        password (str): Senha em texto plano.

    Returns:
        str: Retorna a senha criptografada.

    """
    
    return CRYPTO_CONTEXT.hash(password)
