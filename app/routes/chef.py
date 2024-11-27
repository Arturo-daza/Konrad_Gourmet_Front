from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.categoria_service import CategoriaService
from app.services.inventario_service import InventarioService
from app.services.pedido_service import PedidoService
from app.services.plato_service import PlatoService
from app.services.producto_service import ProductoService
from app.services.unidad_medida_service import UnidadMedidaService

chef_bp = Blueprint("chef", __name__, template_folder="../templates/chef")

@chef_bp.route("/platos", methods=["GET"])
def listar_platos():
    """
    Lista los platos registrados y prepara los datos para mostrar los detalles en el modal.
    """
    platos = PlatoService.obtener_platos()
    categorias = CategoriaService.obtener_categorias()
    unidades = UnidadMedidaService.obtener_unidades()

    # Crear diccionarios para acceso rápido a categorías y unidades
    categorias_dict = {c["id_categoria"]: c for c in categorias}
    unidades_dict = {u["id_unidad"]: u for u in unidades}

    # Recopilar todos los IDs de productos necesarios
    producto_ids = set()
    for plato in platos:
        for ingrediente in plato["ingredientes"]:
            producto_ids.add(ingrediente["id_producto"])

    # Obtener todos los productos en una sola llamada
    productos = ProductoService.obtener_productos_list(list(producto_ids))
    productos_dict = {p["id_producto"]: p for p in productos}

    # Enriquecer los ingredientes con nombres de productos, categorías y unidades
    for plato in platos:
        for ingrediente in plato["ingredientes"]:
            producto = productos_dict.get(ingrediente["id_producto"])
            if producto:
                ingrediente["nombre_producto"] = producto["nombre"]
                ingrediente["nombre_categoria"] = categorias_dict.get(
                    producto["id_categoria"], {"nombre": "Desconocida"}
                )["nombre"]
            else:
                ingrediente["nombre_producto"] = "Desconocido"
                ingrediente["nombre_categoria"] = "Desconocida"

            ingrediente["nombre_unidad"] = unidades_dict.get(
                ingrediente["id_unidad_medida"], {"nombre": "Desconocida"}
            )["nombre"]

    return render_template("chef/platos.html", platos=platos)


@chef_bp.route("/platos/crear", methods=["GET", "POST"])
def crear_plato():
    """
    Crea un nuevo plato.
    """
    categorias = CategoriaService.obtener_categorias()
    unidades = UnidadMedidaService.obtener_unidades()
    productos_organizados = ProductoService.obtener_productos_organizados()

    if request.method == "POST":
        # Validar que haya ingredientes
        ingredientes = request.form.getlist("id_producto[]")
        if not ingredientes or len(ingredientes) == 0:
            flash("Debes agregar al menos un ingrediente.", "error")
            return render_template(
                "chef/crear_plato.html",
                categorias=categorias,
                unidades=unidades,
                productos=productos_organizados,
            )

        data = {
            "nombre": request.form["nombre"],
            "precio": float(request.form["precio"]),
            "ingredientes": []
        }
        # Procesar los ingredientes
        for i in range(len(ingredientes)):
            ingrediente = {
                "id_producto": int(request.form.getlist("id_producto[]")[i]),
                "cantidad": float(request.form.getlist("cantidad[]")[i]),
                "id_unidad_medida": int(request.form.getlist("id_unidad_medida[]")[i]),
            }
            data["ingredientes"].append(ingrediente)

        # Crear el plato usando el servicio
        try:
            PlatoService.crear_plato(data)
            flash("Plato creado exitosamente.", "success")
            return redirect(url_for("chef.listar_platos"))
        except Exception as e:
            flash(f"Error al crear el plato: {str(e)}", "error")
    
    return render_template(
        "chef/crear_plato.html",
        categorias=categorias,
        unidades=unidades,
        productos=productos_organizados
    )

@chef_bp.route("/platos/<int:id_plato>/editar/", methods=["GET", "POST"])
@chef_bp.route("/platos/<int:id_plato>/editar", methods=["GET", "POST"])
def editar_plato(id_plato):
    """
    Edita un plato existente.
    """
    
    try:
        plato = PlatoService.obtener_plato(id_plato)  # Intentar obtener el plato
        if not plato:
            flash("El plato solicitado no existe.", "error")
            return redirect(url_for("chef.listar_platos"))  # Redirigir si no existe
    except Exception as e:
        flash("Error al intentar cargar el plato: {}".format(str(e)), "error")
        return redirect(url_for("chef.listar_platos"))
    
    categorias = CategoriaService.obtener_categorias()
    unidades = UnidadMedidaService.obtener_unidades()
    productos_organizados = ProductoService.obtener_productos_organizados()

    # Enriquecer ingredientes con información adicional (categoría y nombres)
    for ingrediente in plato["ingredientes"]:
        producto = ProductoService.obtener_producto(ingrediente["id_producto"])
        ingrediente["id_categoria"] = producto["id_categoria"]
        ingrediente["nombre_producto"] = producto["nombre"]
        ingrediente["nombre_categoria"] = next(
            (c["nombre"] for c in categorias if c["id_categoria"] == producto["id_categoria"]), "Desconocido"
        )

    if request.method == "POST":
        ingredientes = request.form.getlist("id_producto[]")
        if not ingredientes or len(ingredientes) == 0:
            flash("Debes agregar al menos un ingrediente.", "error")
            return render_template(
                "chef/editar_plato.html",
                plato=plato,
                categorias=categorias,
                unidades=unidades,
                productos=productos_organizados,
            )

        data = {
            "nombre": request.form["nombre"],
            "precio": float(request.form["precio"]),
            "ingredientes": []
        }
        for i in range(len(ingredientes)):
            ingrediente = {
                "id_producto": int(request.form.getlist("id_producto[]")[i]),
                "cantidad": float(request.form.getlist("cantidad[]")[i]),
                "id_unidad_medida": int(request.form.getlist("id_unidad_medida[]")[i]),
            }
            data["ingredientes"].append(ingrediente)

        try:
            PlatoService.actualizar_plato(id_plato, data)
            flash("Plato actualizado exitosamente.", "success")
            return redirect(url_for("chef.listar_platos"))
        except Exception as e:
            flash(f"Error al actualizar el plato: {str(e)}", "error")
    
    return render_template(
        "chef/editar_plato.html",
        plato=plato,
        categorias=categorias,
        unidades=unidades,
        productos=productos_organizados
    )



@chef_bp.route("/platos/<int:id_plato>/eliminar", methods=["POST"])
def eliminar_plato(id_plato):
    """
    Elimina un plato existente.
    """
    PlatoService.eliminar_plato(id_plato)
    flash("Plato eliminado exitosamente.", "success")
    return redirect(url_for("chef.listar_platos"))

@chef_bp.route("/pedidos/<int:id_pedido>/estado", methods=["POST"])
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

@chef_bp.route("/inventario", methods=["GET"])
def listar_inventario():
    id_sucursal = 1  # Es la sucursal principal por defecto
    inventario = InventarioService.obtener_inventario(id_sucursal)
    page = request.args.get("page", default=1, type=int)
    per_page = 10
    total_items = len(inventario)  # Cantidad total de registros
    total_pages = (total_items + per_page - 1) // per_page

    inventario_paginado = inventario[(page - 1) * per_page: page * per_page]

    return render_template(
        "chef/listar_inventario.html",
        inventario=inventario_paginado,
        page=page,
        total_pages=total_pages,
    )


@chef_bp.route("/inventario/crear", methods=["GET", "POST"])
def crear_inventario():
    """
    Crea un nuevo registro de inventario junto con un producto asociado.
    """
    categorias = CategoriaService.obtener_categorias()
    unidades = UnidadMedidaService.obtener_unidades()

    if request.method == "POST":
        # Crear el producto
        producto_data = {
            "nombre": request.form["nombre"],
            "id_categoria": int(request.form["id_categoria"]),
            "id_unidad_medida": int(request.form["id_unidad_medida"]),
            "precio": float(request.form["precio"])
        }

        try:
            producto = ProductoService.crear_producto(producto_data)
        except Exception as e:
            flash(f"Error al crear producto: {str(e)}", "error")
            return render_template("chef/crear_inventario.html", categorias=categorias, unidades=unidades)

        # Crear el inventario
        inventario_data = {
            "id_producto": producto["id_producto"],
            "id_sucursal": 1,  # ID de la sucursal predeterminada
            "cantidad_disponible": int(request.form["cantidad_disponible"]),
            "cantidad_maxima": int(request.form["cantidad_maxima"])
        }

        try:
            InventarioService.crear_inventario(inventario_data)
            flash("Inventario creado exitosamente.", "success")
            return redirect(url_for("chef.listar_inventario"))
        except Exception as e:
            flash(f"Error al crear inventario: {str(e)}", "error")

    return render_template("chef/crear_inventario.html", categorias=categorias, unidades=unidades)

@chef_bp.route("/inventario/<int:id_inventario>/editar", methods=["GET", "POST"])
def editar_inventario(id_inventario):
    """
    Editar un inventario específico.
    """
    if request.method == "POST":
        data = {
            "cantidad_disponible": request.form["cantidad_disponible"],
            "cantidad_maxima": request.form["cantidad_maxima"]
        }
        try:
            InventarioService.actualizar_inventario(id_inventario,  request.form["cantidad_disponible"],  request.form["cantidad_maxima"])
            flash("Inventario actualizado exitosamente.", "success")
            return redirect(url_for("chef.listar_inventario"))
        except Exception as e:
            flash(f"Error al actualizar el inventario: {str(e)}", "error")

    inventario = InventarioService.obtener_inventario_por_id(id_inventario)
    return render_template("chef/editar_inventario.html", inventario=inventario)

@chef_bp.route("/inventario/<int:id_inventario>/eliminar", methods=["POST"])
def eliminar_inventario(id_inventario):
    """
    Elimina un registro de inventario.
    """
    try:
        InventarioService.eliminar_inventario(id_inventario)
        flash("Inventario eliminado exitosamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar inventario: {str(e)}", "error")
    return redirect(request.referrer or url_for("chef.listar_inventario"))

@chef_bp.route("/inventario/<int:id_inventario>/recepcionar", methods=["POST"])
def recepcionar_inventario(id_inventario):
    """
    Recepciona unidades al inventario.
    """
    cantidad = int(request.form["cantidad"])
    try:
        InventarioService.recepcionar_unidades(id_inventario, cantidad)
        flash("Unidades recepcionadas exitosamente.", "success")
    except Exception as e:
        flash(f"Error al recepcionar unidades: {str(e)}", "error")
    return redirect(url_for("chef.listar_inventario"))


