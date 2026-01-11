from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request, jsonify
)
from flask_login import login_user, logout_user, login_required

from app import db
from app.models import User, ActorType, Organisation


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Aucun compte trouvé avec cet email.", "danger")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        flash("Connexion réussie.", "success")

        if user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("home.home"))

    return render_template("login.html")


# =========================
# REGISTER (types & organisations dynamiques)
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # 👉 Charger les types d’acteurs actifs
    actor_types = ActorType.query.filter_by(is_active=True).all()

    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        actor_type_id = request.form.get("actor_type_id")
        organisation_id = request.form.get("organisation_id")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Champs obligatoires
        if not all([
            first_name, last_name, email,
            phone, actor_type_id, organisation_id,
            password, confirm_password
        ]):
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for("auth.register"))

        # Mots de passe
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("auth.register"))

        # Email unique
        if User.query.filter_by(email=email).first():
            flash(
                "Un compte avec cet email existe déjà. Veuillez vous connecter.",
                "warning"
            )
            return redirect(url_for("auth.login"))

        # 👉 CAST DES IDS (IMPORTANT)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            actor_type_id=int(actor_type_id),
            organisation_id=int(organisation_id),
            role="USER"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès. Veuillez vous connecter.", "success")
        return redirect(url_for("auth.login"))

    # 👉 Passer actor_types au template
    return render_template(
        "register.html",
        actor_types=actor_types
    )


# =========================
# API : organisations par type d’acteur
# =========================
@auth_bp.route("/organisations/<int:actor_type_id>")
def organisations_by_actor_type(actor_type_id):

    organisations = Organisation.query.filter_by(
        actor_type_id=actor_type_id,
        is_active=True
    ).all()

    return jsonify([
        {"id": org.id, "name": org.name}
        for org in organisations
    ])


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("auth.login"))
