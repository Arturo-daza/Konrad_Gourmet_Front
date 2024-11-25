import requests
from flask import current_app, session

class CategoriaService:
    @staticmethod
    def obtener_categorias():
        """
        Obtiene la lista de categorías desde la API.
        """
        api_url = current_app.config["API_URL"]
        headers = {"Authorization": f"Bearer {session.get('access_token')}"}
        
        response = requests.get(f"{api_url}/categorias/", headers=headers)
        response.raise_for_status()  # Lanza un error si el código de estado no es 2xx
        return response.json()
