from flask import Blueprint, render_template, redirect, flash, url_for, session, request
from app.forms.auth_form import LoginForm
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Muestra el formulario de inicio de sesión y maneja la autenticación."""
    form = LoginForm()
    if form.validate_on_submit():
        print("Formulario válido")
        email = form.email.data
        password = form.password.data

        try:
            # Llamar al servicio para autenticar al usuario
            token = AuthService.autenticar_usuario(email, password)
            # Guardar el token en la sesión
            session["access_token"] = token["access_token"]
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("home"))  # Redirigir al inicio
        except ValueError as e:  # Error de autenticación
            flash(str(e), "danger")
        except Exception as e:  # Otros errores
            flash("Ocurrió un error inesperado. Inténtalo de nuevo.", "danger")
    else:
        if request.method == "POST":
            print("El formulario no es válido.")
            print(form.errors)

    return render_template("auth/login.html", form=form)
