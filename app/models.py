import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db

# to do: hashing das senhas

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index = True, unique = True)
    senha: so.Mapped[str] = so.mapped_column(sa.String(128))
    posts: so.WriteOnlyMapped['Postagem'] = so.relationship(
        back_populates = 'autor', passive_deletes = True
    )


    def to_dict(self) -> dict:
        query = db.select(Postagem)
        user_posts = db.session.scalars(query.where(Postagem.autor == self))
        return {
            "id": self.id,
            "username": self.username,
            "posts": [
                post.to_dict() for post in user_posts
            ]
        }


    def __repr__(self) -> str:
        return f'<User -> {self.username}>'


class Postagem(db.Model):
    __tablename__ = 'postagens'
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    autor: so.Mapped[Usuario] = so.relationship(
        back_populates = 'posts'
    )
    autor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Usuario.id), index = True)
    postagem: so.Mapped[str] = so.mapped_column(sa.String(324), index = True)
    data: so.Mapped[datetime] = so.mapped_column(index = True, default = lambda: datetime.now(timezone.utc))


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "autor": self.autor.username,
            "postagem": self.postagem
        }


    def __repr__(self) -> str:
        return f'<Post -> {self.postagem}>'


