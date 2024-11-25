import requests
from flask import current_app, session

class PlatoService:
    @staticmethod
    def obtener_encabezados():
        """
        Devuelve los encabezados con el token de autorización.
        """
        token = session.get("access_token")  # Obtener el token de la sesión
        if not token:
            raise ValueError("Token no encontrado en la sesión.")
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def obtener_platos():
        """
        Obtiene la lista de platos desde el API.
        """
        api_url = current_app.config["API_URL"]
        headers = PlatoService.obtener_encabezados()
        response = requests.get(f"{api_url}/platos/", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def obtener_plato(id_plato):
        """
        Obtiene un plato específico por ID desde el API.
        """
        api_url = current_app.config["API_URL"]
        headers = PlatoService.obtener_encabezados()
        response = requests.get(f"{api_url}/platos/{id_plato}", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def crear_plato(data):
        """
        Crea un nuevo plato a través del API.
        """
        api_url = current_app.config["API_URL"]
        headers = PlatoService.obtener_encabezados()
        print(data)
        response = requests.post(f"{api_url}/platos/", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def actualizar_plato(id_plato, data):
        """
        Actualiza un plato existente a través del API.
        """
        api_url = current_app.config["API_URL"]
        headers = PlatoService.obtener_encabezados()
        response = requests.put(f"{api_url}/platos/{id_plato}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def eliminar_plato(id_plato):
        """
        Elimina un plato existente a través del API.
        """
        api_url = current_app.config["API_URL"]
        headers = PlatoService.obtener_encabezados()
        response = requests.delete(f"{api_url}/platos/{id_plato}", headers=headers)
        response.raise_for_status()
