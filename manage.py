"""
运行网站需要进入这个文件目录
"""
from apps import create_app

app = create_app('config.cfg')


if __name__ == '__main__':
    app.run()
