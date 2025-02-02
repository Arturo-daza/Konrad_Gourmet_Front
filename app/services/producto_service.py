import requests
from flask import current_app, session


class ProductoService:
    """
    Servicio para interactuar con el API de productos.
    """

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
    def obtener_productos():
        """
        Obtiene todos los productos desde el API.
        """
        api_url = current_app.config["API_URL"]
        headers = ProductoService.obtener_encabezados()
        response = requests.get(f"{api_url}/productos/", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def obtener_productos_list(ids_producto):
        api_url = current_app.config["API_URL"]
        headers = ProductoService.obtener_encabezados()
        response = requests.post(f"{api_url}/productos/batch", json={"ids_producto": ids_producto}, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            # Manejo de errores según sea necesario
            return []

    @staticmethod
    def obtener_productos_organizados():
        """
        Obtiene todos los productos y los organiza por categoría.
        """
        productos = ProductoService.obtener_productos()
        productos_por_categoria = {}

        for producto in productos:
            categoria_id = producto["id_categoria"]
            if categoria_id not in productos_por_categoria:
                productos_por_categoria[categoria_id] = []
            productos_por_categoria[categoria_id].append(producto)

        return productos_por_categoria

    @staticmethod
    def obtener_producto(id_producto):
        """
        Obtiene un producto específico por ID desde el API.
        """
        api_url = current_app.config["API_URL"]
        headers = ProductoService.obtener_encabezados()
        response = requests.get(f"{api_url}/productos/{id_producto}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def crear_producto(data):
        token = session.get("access_token")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(f"{current_app.config['API_URL']}/productos/", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

