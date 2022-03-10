from apps.views.mall import mall
from apps.views.auto import auto
from apps.views.book import book
from apps.views.blog import blog


def register_blueprints(app):
    """
        加载蓝图
        app.register_blueprint(user, url_prefix='/user')  # 注册user蓝图，并指定前缀。
    :param app:
    :return:
    """

    app.register_blueprint(auto, url_prefix='/auto')  # 用户登录注册
    app.register_blueprint(mall, url_prefix='/mall')
    app.register_blueprint(book, url_prefix='/book')
    app.register_blueprint(blog, url_prefix='/blog')
