import requests
from flask import current_app

class UserService:
    @staticmethod
    def obtener_usuarios():
        """
        Llama al endpoint para obtener la lista de usuarios.
        """
        api_url = current_app.config["API_URL"]
        response = requests.get(f"{api_url}/usuarios/")
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def crear_usuario(data):
        """
        Crea un nuevo usuario mediante la API.
        """
        api_url = current_app.config["API_URL"]
        response = requests.post(f"{api_url}/usuarios/", json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()

class RoleService:
    @staticmethod
    def obtener_roles():
        """
        Llama al endpoint para obtener la lista de roles.
        """
        # api_url = current_app.config["API_URL"]
        # response = requests.get(f"{api_url}/usuarios/roles")
        
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     response.raise_for_status()
        
        return [
                {"id_rol": 1, "nombre": "Administrador"},
                {"id_rol": 2, "nombre": "Jefe de Cocina"},
                {"id_rol": 3, "nombre": "Mesero"},
            ]
        
