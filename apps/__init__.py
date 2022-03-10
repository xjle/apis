from flask import Flask
from apps.ext import register_ext
from apps.views import register_blueprints


def create_app(cfg):
    """  系统初始化   """

    # 初始化 Flask Application
    app = Flask(__name__)

    # 加载配置文件,默认使用 apps/config.cfg
    app.config.from_pyfile(cfg)

    # 初始外部化扩展程序
    register_ext(app)

    # 注册蓝图
    register_blueprints(app)

    return app
