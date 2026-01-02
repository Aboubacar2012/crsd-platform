from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

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

        # Email inexistant
        if not user:
            flash("Aucun compte trouvé avec cet email.", "danger")
            return redirect(url_for("auth.login"))

        # Mot de passe incorrect
        if not user.check_password(password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for("auth.login"))

        # ✅ Connexion réussie
        login_user(user, remember=remember)
        flash("Connexion réussie.", "success")
        # REDIRECTION SELON LE RÔLE
        if user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("home.home"))

    return render_template("login.html")


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        actor_type = request.form.get("actor_type")
        organisation = request.form.get("organisation")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Champs obligatoires
        if not all([
            first_name, last_name, email,
            phone, actor_type, organisation,
            password, confirm_password
        ]):
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for("auth.register"))

        # Mots de passe différents
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("auth.register"))

        # Email déjà existant
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Un compte avec cet email existe déjà. Veuillez vous connecter.", "warning")
            return redirect(url_for("auth.login"))

        # Création utilisateur
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            actor_type=actor_type,
            organisation=organisation,
            role="USER"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès. Veuillez vous connecter.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("auth.login"))
