from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.categoria_service import CategoriaService
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

    # Enriquecer los ingredientes con nombres de productos, categorías y unidades
    for plato in platos:
        for ingrediente in plato["ingredientes"]:
            producto = ProductoService.obtener_producto(ingrediente["id_producto"])
            ingrediente["nombre_producto"] = producto["nombre"]
            ingrediente["nombre_categoria"] = next(
                (c["nombre"] for c in categorias if c["id_categoria"] == producto["id_categoria"]), "Desconocida"
            )
            ingrediente["nombre_unidad"] = next(
                (u["nombre"] for u in unidades if u["id_unidad"] == ingrediente["id_unidad_medida"]), "Desconocida"
            )

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
