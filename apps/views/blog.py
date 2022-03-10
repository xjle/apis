from flask import Blueprint, request
from apps.views.auto import login_required
from apps.models.blog import Blog
from datetime import datetime
from bson import ObjectId
from apps.ext import mongo
import re


blog = Blueprint("blog", __name__)


@blog.route("/find/", methods=["GET", "POST"])
@login_required
def find_blog():
    """
    常用操作符
    * ne 不等于  age__ne=18
    * gt(e) 大于(等于) create_time__gte="2020-03-04 12:07:04"
    * lt(e) 小于(等于) create_time__lte="2020-03-04 12:07:04"
    * not 对操作符取反，比如 age__not__gt=18
    * in 后面是一个列表，比如 city__in=["北京"，"上海"],找出这两个城市的数据，若都不存在，返回空列表。
    * nin in取反  age__nin=[18]
    * mod 取模，比如 age__mod=(2,0) 表示查询出age除以2，余数是0的数据
    :return:
    """
    data = []
    if request.method == "POST":
        return {"code": 401, "msg": "暂不开放"}
        res = mongo.db.Blog.find({"$and": [{"name": {"$regex": request.form.get("name")}}, {"is_del": {"$gt": 0}}]})
        for i in res:
            data.append({"name": i.get("name"), "category": i.get("category"), "create_time": i.get("create_time"),
                         "img": i.get("img"), "update_time": i.get("update_time")})
        return {"code": 200, "msg": "查询成功", "data": data}
    else:
        res = Blog.objects(is_del__ne=0)
        for i in res:
            data.append({"name": i.name, "category": i.category, "create_time": i.create_time, "img": i.img,
                         "update_time": i.update_time})
        return {"code": 200, "msg": "查询成功", "data": data}


@blog.route("/addBlog/", methods=["POST"])
@login_required
def add_blog():
    if request.method == "POST":
        return {"code": 401, "msg": "暂不开放"}
        params = request.form
        b_name = params.get("name")
        b_category = params.get("category")
        b_img = params.get("img")
        if not b_name or not b_category or not b_img:
            return {"code": 401, "msg": "输入不为空"}
        res = Blog.objects(name=b_name).first()
        if res:
            return {"code": 403, "msg": "书籍已存在"}
        else:
            Blog(name=b_name, category=b_category, img=b_img, url="").save()
            return {"code": 200, "msg": "书籍保存成功"}


@blog.route("/updateBlog/", methods=["POST"])
@login_required
def update_blog():
    if request.method == "POST":
        return {"code": 401, "msg": "暂不开放"}
        params = request.form
        b_id = params.get("bid")
        b_name = params.get("name")
        b_category = params.get("category")
        b_img = params.get("img")
        if not b_id and not b_name or not b_category or not b_img:
            return {"code": 401, "msg": "输入不为空"}
        res = Blog.objects(id=ObjectId(b_id)).first()
        res.name = b_name
        res.category = b_category
        res.update_time = datetime.now
        res.save()
        return {"code": 200, "msg": "修改成功"}


@blog.route("/deleteBlog/<bid>/")
@login_required
def delete_blog(bid):
    return {"code": 401, "msg": "暂不开放"}
    res = Blog.objects(id=ObjectId(bid)).first()
    if res:
        res.is_del = 0
        res.update_time = datetime.now
        res.save()
        return {"code": 200, "msg": "删除成功"}
    else:
        return {"code": 403, "msg": "书籍不存在或已删除"}
