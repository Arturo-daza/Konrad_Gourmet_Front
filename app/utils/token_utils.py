import jwt
from flask import current_app, session

def decodificar_token(token: str) -> dict:
    """
    Decodifica el token JWT y extrae los datos.
    :param token: Token JWT
    :return: Diccionario con los datos del token
    """
    secret_key = current_app.config["SECRET_KEY"]
    print(secret_key)
    return jwt.decode(token, secret_key, algorithms=["HS256"])

def guardar_en_session(token: str):
    """
    Decodifica el token JWT y guarda la información en la sesión.
    :param token: Token JWT
    """
    try:
        data = decodificar_token(token)
        session["username"] = data.get("username")
        session["rol"] = data.get("rol")
    except jwt.ExpiredSignatureError:
        raise ValueError("El token ha expirado.")
    except jwt.DecodeError:
        raise ValueError("Token inválido.")
