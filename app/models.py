import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from hashlib import sha256
from datetime import datetime, timezone
from app import db, login


def hash_senha(senha: str):
    hash = sha256()
    hash.update(senha.encode())
    return hash.hexdigest()


@login.user_loader
def load_user(id):
    return db.session.get(Usuario, int(id))


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    matricula: so.Mapped[str] = so.mapped_column(
        sa.String(25), unique=True, index=True
    )
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True
    )
    senha: so.Mapped[str] = so.mapped_column(sa.String(128))

    posts: so.WriteOnlyMapped['Postagem'] = so.relationship(
        back_populates='autor', passive_deletes=True
    )

    def check_senha(self, senha):
        hash = hash_senha(senha)
        if senha == hash:
            return True
        return False

    def to_dict(self) -> dict:
        query = db.select(Postagem)
        user_posts = db.session.scalars(query.where(Postagem.autor == self))

        return {
            "id": self.id,
            "username": self.username,
            "matricula": self.matricula,
            "posts": [post.to_dict() for post in user_posts]
        }

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Postagem(db.Model):
    __tablename__ = 'postagens'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    autor: so.Mapped[Usuario] = so.relationship(
        back_populates='posts'
    )
    autor_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Usuario.id), index=True)
    postagem: so.Mapped[str] = so.mapped_column(sa.String(324), index=True)
    data: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "postagem": self.postagem,
            "autor": self.autor.username,
            "matricula": self.autor.matricula
        }

    def __repr__(self) -> str:
        return f'<Postagem {self.postagem}>'
