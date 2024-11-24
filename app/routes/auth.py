from flask import Blueprint, render_template, redirect, flash, url_for, session
from app.forms.auth_form import LoginForm
from app.services.auth_service import AuthService
from app.utils.token_utils import guardar_en_session

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Muestra el formulario de inicio de sesión y maneja la autenticación."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            # Llamar al servicio para autenticar al usuario
            token = AuthService.autenticar_usuario(email, password)["access_token"]
            # Guardar información del usuario en la sesión
            guardar_en_session(token)

            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("dashboard.dashboard"))  # Redirigir al panel de administración
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash("Ocurrió un error inesperado. Inténtalo de nuevo.", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout", methods=["GET"])
def logout():
    """
    Cierra la sesión del usuario.
    """
    session.clear()  # Elimina todos los datos de la sesión
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("auth.login"))