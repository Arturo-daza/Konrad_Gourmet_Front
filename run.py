from app import create_app
import os

# Crea la instancia de la aplicación Flask
app = create_app()

# Punto de entrada
if __name__ == "__main__":
    # Cargar el puerto desde las variables de entorno o usar 5000 por defecto
    port = int(os.getenv("PORT", 5000))
    # Ejecutar la aplicación
    app.run(host="0.0.0.0", port=port, debug=True)
