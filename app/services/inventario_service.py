from flask import current_app, session
import requests


class InventarioService:
    @staticmethod
    def obtener_inventario(id_sucursal):
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{current_app.config['API_URL']}/inventarios/sucursal/{id_sucursal}", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def actualizar_inventario(id_inventario, cantidad_disponible, cantidad_maxima):
        """
        Actualiza un inventario por su ID.
        """
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "cantidad_disponible": cantidad_disponible,
            "cantidad_maxima": cantidad_maxima
        }
        response = requests.put(f"{current_app.config['API_URL']}/inventarios/{id_inventario}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def crear_inventario(data):
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(f"{current_app.config['API_URL']}/inventarios/", json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def editar_inventario(id_inventario, data):
        """
        Actualiza un registro de inventario existente.
        """
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.put(f"{current_app.config['API_URL']}/inventario/{id_inventario}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def eliminar_inventario(id_inventario):
        """
        Elimina un registro de inventario.
        """
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{current_app.config['API_URL']}/inventario/{id_inventario}", headers=headers)
        response.raise_for_status()
        
    @staticmethod
    def obtener_inventario_por_id(id_inventario):
        """
        Consume el endpoint para obtener un inventario específico.
        """
        token = session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url = f"{current_app.config['API_URL']}/inventarios/{id_inventario}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def recepcionar_unidades(id_inventario, cantidad):
            """
            Consume el endpoint para recepcionar unidades al inventario.
            """
            token = session.get("access_token")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            url = f"{current_app.config['API_URL']}/inventarios/{id_inventario}/recepcionar"
            data = {"cantidad": cantidad}
            response = requests.post(url, params=data, headers=headers)
            response.raise_for_status()
            return response.json()