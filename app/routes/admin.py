from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from app.services.user_service import UserService, RoleService

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

@admin_bp.route("/users", methods=["GET"])
def users():
    """
    Lista los usuarios y permite crear nuevos.
    """
    if session.get("rol") != "Administrador":
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for("dashboard.dashboard"))
    
    # Obtener usuarios y roles desde la API
    usuarios = UserService.obtener_usuarios()
    roles = RoleService.obtener_roles()

    return render_template("admin/users.html", usuarios=usuarios, roles=roles)

@admin_bp.route("/users/create", methods=["POST"])
def create_user():
    """
    Crea un nuevo usuario con los datos enviados desde el formulario.
    """
    data = {
        "nombre": request.form["nombre"],
        "email": request.form["email"],
        "password": request.form["password"],
        "id_rol": int(request.form["id_rol"]),
    }

    try:
        UserService.crear_usuario(data)
        flash("Usuario creado exitosamente.", "success")
    except Exception as e:
        flash(f"Error al crear usuario: {str(e)}", "danger")

    return redirect(url_for("admin.users"))

