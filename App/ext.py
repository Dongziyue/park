from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    """ 初始化所有第三方插件 """
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

