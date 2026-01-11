from app import db


class Organisation(db.Model):
    __tablename__ = "organisations"

    id = db.Column(db.Integer, primary_key=True)

    actor_type_id = db.Column(
        db.Integer,
        db.ForeignKey("actor_types.id"),
        nullable=False
    )

    name = db.Column(db.String(255), nullable=False)

    acronym = db.Column(db.String(50))

    country = db.Column(db.String(100))

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime, server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Organisation {self.name}>"
