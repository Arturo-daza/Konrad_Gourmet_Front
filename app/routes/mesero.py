from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from app.services.pedido_service import PedidoService
from app.services.plato_service import PlatoService
from app.services.producto_service import ProductoService

mesero_bp = Blueprint("mesero", __name__, url_prefix="/mesero")

@mesero_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    """
    Lista todos los pedidos con filtros opcionales por fecha, estado e ID.
    """
    
    # Obtener la fecha de hoy
    fecha_hoy = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Leer parámetros del request o usar valores predeterminados
    fecha = request.args.get("fecha", fecha_hoy)  # Fecha por defecto es "hoy"
    estado = request.args.get("estado")  # Estado puede ser opcional
    mesa = request.args.get("mesa")  # Mesa puede ser opcional
    
    pedidos = PedidoService.obtener_pedidos()
    platos = PlatoService.obtener_platos()  # Obtener todos los platos disponibles

    # Crear un diccionario para mapear id_plato a nombre
    mapa_platos = {plato["id_plato"]: plato["nombre"] for plato in platos}

    # Agregar el nombre del plato a cada detalle de los pedidos
    for pedido in pedidos:
        for detalle in pedido["detalles"]:
            detalle["nombre"] = mapa_platos.get(detalle["id_plato"], "Plato desconocido")

    # Filtrar por fecha
    if fecha:
        pedidos = [pedido for pedido in pedidos if pedido["fecha"].startswith(fecha)]

    # Filtrar por estado
    if estado:
        pedidos = [pedido for pedido in pedidos if pedido["estado"] == estado]

    # Filtrar por ID Pedido
    if mesa:
        pedidos = [pedido for pedido in pedidos if str(pedido["mesa"]) == mesa]

    # Ordenar por estado (Pendiente > Preparado > Entregado > Cancelado)
    orden_estado = {"pendiente": 0, "preparado": 1, "entregado": 2, "cancelado": 3}
    pedidos.sort(key=lambda p: orden_estado.get(p["estado"], 4))

    return render_template("mesero/listar_pedidos.html", pedidos=pedidos,  fecha_hoy=fecha_hoy)



@mesero_bp.route("/pedidos/crear", methods=["GET", "POST"])
def crear_pedido():
    """
    Crea un nuevo pedido. Solo muestra platos que se pueden preparar.
    """
    platos_preparables = PedidoService.obtener_platos_preparables()

    if request.method == "POST":
        data = {
            "mesa": int(request.form["mesa"]),
            "detalles": []
        }

        platos = request.form.getlist("id_plato[]")
        cantidades = request.form.getlist("cantidad[]")

        for i in range(len(platos)):
            id_plato = int(platos[i])
            cantidad = int(cantidades[i])

            # Validar que la cantidad no exceda el máximo preparable
            max_preparable = next((p["cantidad_preparable"] for p in platos_preparables if p["id_plato"] == id_plato), 0)
            if cantidad > max_preparable:
                flash(f"La cantidad para el plato {id_plato} excede el máximo preparable ({max_preparable}).", "error")
                return render_template("mesero/crear_pedido.html", platos_preparables=platos_preparables)

            data["detalles"].append({"id_plato": id_plato, "cantidad": cantidad})

        try:
            PedidoService.crear_pedido(data)
            flash("Pedido creado exitosamente.", "success")
            return redirect(url_for("mesero.listar_pedidos"))
        except Exception as e:
            flash(f"Error al crear el pedido: {str(e)}", "error")

    return render_template("mesero/crear_pedido.html", platos_preparables=platos_preparables)



@mesero_bp.route("/pedidos/<int:id_pedido>/editar", methods=["GET", "POST"])
def editar_pedido(id_pedido):
    """
    Edita un pedido existente.
    """
    pedido = PedidoService.obtener_pedido(id_pedido)

    if request.method == "POST":
        data = {
            "detalles": []
        }

        platos = request.form.getlist("id_plato[]")
        cantidades = request.form.getlist("cantidad[]")

        for i in range(len(platos)):
            detalle = {
                "id_plato": int(platos[i]),
                "cantidad": int(cantidades[i])
            }
            data["detalles"].append(detalle)

        try:
            PedidoService.actualizar_pedido(id_pedido, data)
            flash("Pedido actualizado exitosamente.", "success")
            return redirect(url_for("mesero.listar_pedidos"))
        except Exception as e:
            flash(f"Error al actualizar el pedido: {str(e)}", "error")

    return render_template("mesero/editar_pedido.html", pedido=pedido)

@mesero_bp.route("/pedidos/<int:id_pedido>/eliminar", methods=["POST"])
def eliminar_pedido(id_pedido):
    """
    Elimina un pedido existente.
    """
    try:
        PedidoService.eliminar_pedido(id_pedido)
        flash("Pedido eliminado exitosamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar el pedido: {str(e)}", "error")

    return redirect(url_for("mesero.listar_pedidos"))

@mesero_bp.route("/pedidos/<int:id_pedido>/estado", methods=["POST"])
def actualizar_estado_pedido(id_pedido):
    """
    Actualiza el estado de un pedido.
    """
    nuevo_estado = request.form["estado"]
    try:
        PedidoService.actualizar_estado(id_pedido, {"estado": nuevo_estado})
        flash("Estado del pedido actualizado exitosamente.", "success")
    except Exception as e:
        flash(f"Error al actualizar el estado del pedido: {str(e)}", "error")

    return redirect(url_for("mesero.listar_pedidos"))



