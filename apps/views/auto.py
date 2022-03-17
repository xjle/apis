from flask import Blueprint, g, request, current_app
from apps.utils.tool import Tool
from apps.utils import send_mail as tool_send_mali
from apps.ext import cache
from apps.models.user import User
from apps.models.menu import Menu
import functools

auto = Blueprint("auto", __name__)


def login_required(func):
    """
    登录验证装饰器
    :param func:
    :return:
    """
    data = {"code": 401, "msg": "缺少必要参数"}

    @functools.wraps(func)
    def verify_token(*args, **kwargs):
        try:
            token = request.headers.get("Token")
        except Exception:
            return data

        try:
            # 转换为字典
            res = Tool.verify_token(token)
            g.user = res
            if not res:
                data['code'] = 201
                data['msg'] = '登陆过期'
                return data
        except Exception:
            data['code'] = 201
            data['msg'] = '登陆过期'
            return data
        return func(*args, **kwargs)
    return verify_token


def admin_auth(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):  # 让某个函数来继承我们的参数
        if g.user.get("role") < 100:
            return {"code": 403, "msg": "權限不足"}
        return f(*args, **kwargs)

    return decorated_function


@auto.route("/")
@login_required
def index():
    token = request.headers['token']
    res = Tool.verify_token(token)
    user = User.objects(id=res.get("id")).first()
    menu = Menu.objects(role__lte=g.user.get("role"))
    menu_data = []
    for item in menu:
        menu_data.append({"name": item.name, "mid": item.mid, "url": item.url, "icon": item.icon, "role": item.role,
                          "status": item.status, "create_time": item.create_time, "update_time": item.update_time})
    return {"code": 200, "data": {"mail": user.mail, "wd": user.wd, "nickname": user.nickname, "phone": user.phone,
                                  "level": user.level, "create_time": user.create_time, "update_time": user.update_time,
                                  "role": user.role, "menu": menu_data}}


@auto.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        params = request.form
        mail = params.get("mail")
        password = params.get("password")
        code = params.get("code")
        if not mail or not password or not code:
            return {"code": 401, "msg": "输入不为空"}
        cache_code = "9527"
        # cache.get(mail)
        if cache_code and cache_code == code:
            user = User.objects(mail=mail).first()
            if user:
                if Tool.decrypt(password, user.password):
                    token = Tool.create_token({'id': user.id, 'mail': user.mail, 'role': user.role})
                    return {"code": 200, "msg": "登录成功", "data": {"token": token}}
                else:
                    return {"code": 403, "msg": "密码错误"}
            else:
                return {"code": 401, "msg": "账号未注册"}
        else:
            return {"code": 403, "msg": "验证码错误或失效"}


@auto.route("/send/", methods=["POST"])
def send_mail():
    if request.method == 'POST':
        mail = request.form.get("mail")
        if not mail:
            return {"code": 401, "msg": "邮箱不为空"}
        if not cache.get(mail):
            code = Tool.get_verification(6, False)
            send_ret = tool_send_mali(subject="验证码", recipient=mail, body="验证码为{}".format(code))
            if send_ret:
                cache.set(mail, code)
                return {"code": 200, "msg": "发送成功"}
            else:
                return {"code": 403, "msg": "发送失败"}
        else:
            return {"code": 403, "msg": "请不要重复请求"}


@auto.route("/register/", methods=["POST"])
def register():
    if request.method == "POST":
        # 获取表单数据
        mail = request.form.get("mail")
        password = request.form.get("password")
        code = request.form.get("code")
        if not mail or not password or not code:
            return {"code": 401, "msg": "输入不为空"}
        # 查找数据
        ret = User.objects(mail=mail).first()
        if not ret:
            cache_code = cache.get(mail)
            if cache_code and cache_code == code:
                User(mail=mail, password=Tool.encryption(password)).save()
                return {"code": 200, "msg": "注册成功"}
            else:
                return {"code": 403, "msg": "验证码错误或验证码过期"}
        else:
            return {"code": 403, "msg": "用户已存在"}


@auto.route("/addMenu/", methods=["POST"])
@login_required
@admin_auth
def add_menu():
    if request.method == "POST":
        params = request.form
        mid = params.get("mid")
        name = params.get("name")
        url = params.get("url")
        icon = params.get("icon")
        role = params.get("role")
        if not mid or not name or not url:
            return {"code": 401, "msg": "缺失参数"}
        try:
            Menu(mid=mid, name=name, url="admin/" + url, icon=icon, role=role).save()
        except:
            return {"code": 403, "msg": "参数错误"}
        return {"code": 200, "msg": "添加成功"}


@auto.route("/deleteMenu/<mid>")
@login_required
@admin_auth
def del_menu(mid):
    if not mid:
        return {"code": 401, "msg": "缺失参数"}
    menu = Menu.objects().get(mid=mid)
    if menu:
        menu.status = False
        menu.save()
        return {"code": 200, "msg": "删除成功"}
    else:

        return {"code": 403, "msg": "参数错误"}


@auto.route("/updateUserInfo/", methods=["POST"])
@login_required
def update_userinfo():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        user = User.objects().get(id=g.user.id)
        if user:
            user.nickname = nickname
            user.save()
            return {"code": 200, "msg": "修改成功"}
        else:
            """按理不会跳转"""
            return {"code": 403, "msg": "参数错误"}
