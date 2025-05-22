from datetime import datetime
from flask import Flask, current_app
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import click
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()

db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)

    # formatar saídas e identificar representação
    def __repr__(self)-> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str]= mapped_column(sa.String, unique=True, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    # formatar saídas e identificar representação
    def __repr__(self)-> str:
        return f"Post(id={self.id!r}, title={self.username!r}, author_id={self.author_id!r})"





@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    
    click.echo('Initialized the database.')

# implementation of the Flask application and conection to the database
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite",
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
   
    app.cli.add_command(init_db_command)

    db.init_app(app)


    #register blueprints
    from src.controllers import user
    from src.controllers import post
    app.register_blueprint(user.app)

    return app
     