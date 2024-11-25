import requests
from flask import current_app, session

class UnidadMedidaService:
    @staticmethod
    def obtener_unidades():
        """
        Obtiene la lista de unidades de medida desde la API.
        """
        # api_url = current_app.config["API_URL"]
        # headers = {"Authorization": f"Bearer {session.get('access_token')}"}
        
        # response = requests.get(f"{api_url}/unidades/", headers=headers)
        # response.raise_for_status()  # Lanza un error si el código de estado no es 2xx
        # return response.json()
        return [
            {"id_unidad": 1, "nombre": "Kilogramo"},
            {"id_unidad": 2, "nombre": "Gramo"},
            {"id_unidad": 3, "nombre": "Litro"},
            {"id_unidad": 4, "nombre": "Mililitro"},
            {"id_unidad": 5, "nombre": "Unidad"},
            {"id_unidad": 6, "nombre": "Libra"},
        ]
