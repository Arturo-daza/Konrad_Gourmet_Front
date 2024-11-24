import requests
from flask import current_app

class AuthService:
    @staticmethod
    def autenticar_usuario(email: str, password: str):
        """
        Llama al endpoint de autenticación para obtener un token.
        :param email: Correo del usuario.
        :param password: Contraseña del usuario.
        :return: Token de autenticación si las credenciales son válidas.
        """
        api_url = current_app.config["API_URL"]
        endpoint = f"{api_url}/auth/token"

        params = {
            "username": email,
            "password": password
        }

        response = requests.post(endpoint, params=params)

        if response.status_code == 200:
            return response.json()  # Devuelve el token
        elif response.status_code == 401:  # Credenciales inválidas
            raise ValueError("Correo o contraseña incorrectos.")
        else:
            response.raise_for_status()  # Lanza otros errores
