from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from functools import wraps

from app import db
from app.models import User, ActorType, Organisation

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
# ADMIN ACCESS DECORATOR
# =========================
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "ADMIN":
            abort(403)
        return func(*args, **kwargs)
    return wrapper


# =========================
# DASHBOARD
# =========================
@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {
        "total_users": User.query.count(),
        "admins": User.query.filter_by(role="ADMIN").count(),
        "users": User.query.filter_by(role="USER").count(),
        "actor_types": ActorType.query.count(),
        "organisations": Organisation.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


# =========================
# USERS MANAGEMENT
# =========================
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/<int:user_id>/toggle-role")
@login_required
@admin_required
def toggle_role(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Vous ne pouvez pas modifier votre propre rôle.", "warning")
        return redirect(url_for("admin.users"))

    user.role = "ADMIN" if user.role == "USER" else "USER"
    db.session.commit()

    flash("Rôle utilisateur mis à jour.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/delete")
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "danger")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()

    flash("Utilisateur supprimé.", "success")
    return redirect(url_for("admin.users"))


# =========================
# ACTOR TYPES (CRUD)
# =========================
@admin_bp.route("/actor-types")
@login_required
@admin_required
def actor_types():
    actor_types = ActorType.query.order_by(ActorType.id.asc()).all()
    return render_template("admin/actor_types.html", actor_types=actor_types)


@admin_bp.route("/actor-types/add", methods=["POST"])
@login_required
@admin_required
def add_actor_type():
    code = request.form.get("code")
    label = request.form.get("label")

    if not code or not label:
        flash("Code et libellé obligatoires.", "danger")
        return redirect(url_for("admin.actor_types"))

    code = code.upper()

    if ActorType.query.filter_by(code=code).first():
        flash("Ce type d’acteur existe déjà.", "warning")
        return redirect(url_for("admin.actor_types"))

    actor_type = ActorType(
        code=code,
        label=label.upper(),
        is_active=True
    )

    db.session.add(actor_type)
    db.session.commit()

    flash("Type d’acteur ajouté.", "success")
    return redirect(url_for("admin.actor_types"))


@admin_bp.route("/actor-types/<int:id>/toggle")
@login_required
@admin_required
def toggle_actor_type(id):
    actor_type = ActorType.query.get_or_404(id)
    actor_type.is_active = not actor_type.is_active
    db.session.commit()

    flash("Statut du type d’acteur mis à jour.", "success")
    return redirect(url_for("admin.actor_types"))


# =========================
# ORGANISATIONS
# =========================
@admin_bp.route("/organisations")
@login_required
@admin_required
def organisations():
    organisations = Organisation.query.order_by(Organisation.id.desc()).all()
    actor_types = ActorType.query.filter_by(is_active=True).all()

    return render_template(
        "admin/organisations.html",
        organisations=organisations,
        actor_types=actor_types
    )


@admin_bp.route("/organisations/add", methods=["POST"])
@login_required
@admin_required
def add_organisation():
    name = request.form.get("name")
    actor_type_id = request.form.get("actor_type_id")

    if not name or not actor_type_id:
        flash("Nom et type d’acteur obligatoires.", "danger")
        return redirect(url_for("admin.organisations"))

    organisation = Organisation(
        name=name.strip(),
        actor_type_id=int(actor_type_id),
        is_active=True
    )

    db.session.add(organisation)
    db.session.commit()

    flash("Organisation ajoutée.", "success")
    return redirect(url_for("admin.organisations"))


@admin_bp.route("/organisations/<int:organisation_id>/edit", methods=["POST"])
@login_required
@admin_required
def edit_organisation(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)

    name = request.form.get("name")
    actor_type_id = request.form.get("actor_type_id")

    if not name or not actor_type_id:
        flash("Nom et type d’acteur obligatoires.", "danger")
        return redirect(url_for("admin.organisations"))

    organisation.name = name.strip()
    organisation.actor_type_id = int(actor_type_id)

    db.session.commit()
    flash("Organisation modifiée avec succès.", "success")
    return redirect(url_for("admin.organisations"))


@admin_bp.route("/organisations/toggle/<int:organisation_id>")
@login_required
@admin_required
def toggle_organisation(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)
    organisation.is_active = not organisation.is_active

    db.session.commit()
    flash("Statut de l’organisation modifié.", "success")
    return redirect(url_for("admin.organisations"))


# =========================
# DELETE ORGANISATION (SECURISÉ)
# =========================
@admin_bp.route("/organisations/<int:organisation_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_organisation(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)

    confirmation = request.form.get("confirmation", "").strip()

    # DEBUG TEMPORAIRE (tu pourras enlever après validation)
    print(f"[DELETE ORG] {organisation.id=} {organisation.name=} {confirmation=}")

    if confirmation != "SUPPRIMER":
        flash("Confirmation invalide. Tapez SUPPRIMER pour confirmer.", "danger")
        return redirect(url_for("admin.organisations"))

    db.session.delete(organisation)
    db.session.commit()

    flash("Organisation supprimée définitivement.", "success")
    return redirect(url_for("admin.organisations"))


# =========================
# MODULES (placeholder)
# =========================
@admin_bp.route("/modules")
@login_required
@admin_required
def modules():
    return render_template("admin/modules.html")


# =========================
# SETTINGS
# =========================
@admin_bp.route("/settings")
@login_required
@admin_required
def settings():
    return render_template("admin/settings.html")
