import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import sha256
from datetime import datetime, timezone
from app import db


def hash_senha(senha: str):
    hash = sha256()
    hash.update(senha.encode())
    return hash.hexdigest()


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    matricula: so.Mapped[str] = so.mapped_column(sa.String(25), unique=True, index=True)
    senha: so.Mapped[str] = so.mapped_column(sa.String(128))

    posts: so.WriteOnlyMapped['Postagem'] = so.relationship(back_populates='autor', passive_deletes=True)
    noticias: so.WriteOnlyMapped['Noticia'] = so.relationship(back_populates='autor', passive_deletes=True)

    servidor: so.Mapped[bool] = so.mapped_column(nullable=False)


    @property
    def is_servidor(self) -> bool:
        return self.servidor


    def check_senha(self, senha):
        hash = hash_senha(senha)

        return True if senha == hash else False


    def to_dict(self):
        return {
            "id": self.id,
            "matricula": self.matricula,
            "username": self.username,
            "servidor": self.is_servidor
        }


    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Postagem(db.Model):
    __tablename__ = 'postagens'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    autor: so.Mapped[Usuario] = so.relationship(back_populates='posts')
    matricula: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Usuario.matricula))

    postagem: so.Mapped[str] = so.mapped_column(sa.String(324), index=True)
    data: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    id_fundo: so.Mapped[int] = so.mapped_column(sa.Integer)


    def to_dict(self):
        return {
            "id": self.id,
            "matricula": self.matricula,
            "postagem": self.postagem,
            "data": self.data
        }

    def __repr__(self) -> str:
        return f'<Postagem {self.postagem}>'


class Noticia(db.Model):
    __tablename__ = "noticias"

    id: so.Mapped[int] = so.mapped_column(primary_key = True)

    autor: so.Mapped[Usuario] = so.relationship(back_populates='noticias')
    autor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Usuario.id))

    setor: so.Mapped[str] = so.mapped_column(sa.String(32))
    titulo: so.Mapped[str] = so.mapped_column(sa.String(64))
    corpo: so.Mapped[str] = so.mapped_column(sa.String(324))

    imagem: so.Mapped[str] = so.mapped_column(sa.String(324), nullable=True)
    link: so.Mapped[str] = so.mapped_column(sa.String(324), nullable=True)
