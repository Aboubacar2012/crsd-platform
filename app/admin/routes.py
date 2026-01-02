from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models.user import User
from app import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
# ADMIN ACCESS CONTROL
# =========================
def admin_required():
    """
    Vérifie que l'utilisateur est authentifié ET admin.
    """
    if not current_user.is_authenticated or current_user.role != "ADMIN":
        abort(403)


# =========================
# USERS MANAGEMENT
# =========================
@admin_bp.route("/users")
@login_required
def users():
    admin_required()
    users = User.query.order_by(User.created_at.desc() if hasattr(User, "created_at") else User.id.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/<int:user_id>/toggle-role")
@login_required
def toggle_role(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)

    # Empêcher l'admin de se modifier lui-même
    if user.id == current_user.id:
        flash("Vous ne pouvez pas modifier votre propre rôle.", "warning")
        return redirect(url_for("admin.users"))

    # Toggle USER <-> ADMIN
    user.role = "ADMIN" if user.role == "USER" else "USER"

    db.session.commit()
    flash("Rôle utilisateur mis à jour avec succès.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/delete")
@login_required
def delete_user(user_id):
    admin_required()

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "danger")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("admin.users"))


# =========================
# ACTOR TYPES (STRUCTURE)
# =========================
@admin_bp.route("/actor-types")
@login_required
def actor_types():
    admin_required()
    return render_template("admin/actor_types.html")


# =========================
# ORGANISATIONS (STRUCTURE)
# =========================
@admin_bp.route("/organisations")
@login_required
def organisations():
    admin_required()
    return render_template("admin/organisations.html")


# =========================
# CONTEXT DATABASE
# =========================
@admin_bp.route("/settings")
@login_required
def settings():
    admin_required()
    return render_template("admin/settings.html")


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    admin_required()

    stats = {
        "total_users": User.query.count(),
        "admins": User.query.filter_by(role="ADMIN").count(),
        "users": User.query.filter_by(role="USER").count(),
    }

    return render_template("admin/dashboard.html", stats=stats)
