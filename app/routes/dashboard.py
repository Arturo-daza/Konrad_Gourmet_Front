from flask import Blueprint, render_template, session, redirect, flash, url_for

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates/dashboard")

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Vista general del dashboard. Filtra la información según el rol del usuario.
    """
    if "rol" not in session:
        flash("Debes iniciar sesión para acceder al dashboard.", "danger")
        return redirect(url_for("auth.login"))
    
    # Rol del usuario
    rol = session["rol"]

   

    return render_template("dashboard/general.html")
