import requests
from flask import current_app, session

class PedidoService:
    @staticmethod
    def obtener_pedidos():
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{current_app.config['API_URL']}/pedidos", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def obtener_pedido(id_pedido):
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{current_app.config['API_URL']}/pedidos/{id_pedido}", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def crear_pedido(data):
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{current_app.config['API_URL']}/pedidos", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def actualizar_pedido(id_pedido, data):
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.put(f"{current_app.config['API_URL']}/pedidos/{id_pedido}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def actualizar_estado(id_pedido, data):
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.put(f"{current_app.config['API_URL']}/pedidos/{id_pedido}/estado", params=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def eliminar_pedido(id_pedido):
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{current_app.config['API_URL']}/pedidos/{id_pedido}", headers=headers)
        response.raise_for_status()
        
    @staticmethod
    def obtener_platos_preparables():
        """
        Obtiene los platos que se pueden preparar según el inventario.
        """
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{current_app.config['API_URL']}/platos/acciones/preparables", headers=headers)
        response.raise_for_status()
        return response.json()
        
