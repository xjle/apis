from flask import Blueprint, request
from bson import ObjectId
from apps.ext import mongo
import re


book = Blueprint("book", __name__)


@book.route("/")
def index():
    """
    测试接口：
        获取分类
        获取轮播图
        获取广告位
        获取猜你喜欢：暂无
    :return:
    """
    book_db = mongo.db.category
    res = book_db.find()
    data = []
    for i in res:
        obj = {"id": str(i.get("_id")), "title": i.get("category"), "level": i.get("level")}
        data.append(obj)
    banner = [{"img": "http://img61.ddimg.cn/2022/2/28/20220228182557262.jpg"},
              {"img": "http://img60.ddimg.cn/upload_img/00822/cxtc/750x315_wzh_20220302-1646287066.jpg"},
              {"img": "http://img62.ddimg.cn/upload_img/00316/by/13536p-1646360554.jpg"}]
    lovely = ""  # 暂无
    advertisement = [{"img": "http://img63.ddimg.cn/upload_img/00814/2/382x140-1620893021.jpg"},
                     {"img": "http://img63.ddimg.cn/topic_img/gys_06486/2022ckx382x140.jpg"},
                     {"img": "http://img61.ddimg.cn/upload_img/00785/ts/8810-1605865600.jpg"}]
    return {"data": data, "banner": banner, "advertisement": advertisement, "code": 200}


@book.route("/category/", methods=["POST"])
def category():
    """
    测试接口
        根据分类id展示
    :return:
    """
    if request.method == "POST":
        book_db = mongo.db.category
        params = request.form
        data = []
        category_id = params.get("id")
        res = book_db.find({"_id": ObjectId(category_id)})
        for i in res:
            for item in i.get("children"):
                obj = {"id": item.get("id"), "title": item.get("title"), "img": item.get("img"),
                       "price": item.get("price"), "author": item.get("author")}
                data.append(obj)
        return {"data": data, "code": 200}


@book.route("/search/")
def search():
    """
    测试接口
        搜索书名
    :return:
    """
    params = request.args
    kw = params.get("kw")
    book_db = mongo.db.category
    data = []
    res = book_db.aggregate([{"$unwind": "$children"}, {"$match": {'children.title': re.compile(r"" + kw + "")}}])
    for i in res:
        item = i.get("children")
        obj = {"id": item.get("id"), "title": item.get("title"), "img": item.get("img"), "author": item.get("author"),
               "price": item.get("price")}
        data.append(obj)
    return {"data": data, "code": 200}


@book.route("/detail/<bid>")
def detail(bid):
    """
    测试接口
        详情
    :param bid:
    :return:
    """
    book_db = mongo.db.category
    data = []
    res = book_db.aggregate([{"$unwind": "$children"}, {"$match": {'children.id': bid}}])
    for i in res:
        item = i.get("children")
        obj = {"id": item.get("id"), "title": item.get("title"), "img": item.get("img"), "author": item.get("author"),
               "price": item.get("price"), "publisher": item.get("publisher"), "count_per": item.get("count_per"),
               "publisher_time": item.get("publisher_time"), "publisher_nums": item.get("publisher_nums"),
               "catalogue": item.get("catalogue"), "stock": item.get("stock"), "desc": item.get("desc"),
               "bi": item.get("d_d")}
        data.append(obj)
    return {"data": data, "code": 200}
