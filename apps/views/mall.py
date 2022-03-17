from datetime import datetime
import random

from flask import Blueprint, render_template, request, g

from apps.views.auto import login_required
from apps.utils.tool import Tool
from apps.ext import mongo
from flask_caching import Cache

mall = Blueprint('mall', __name__)
cache = Cache()


@mall.route("/car/", methods=["GET", "POST"])
@login_required
def car():
    """
    测试接口
        购物车 --不限量库存
            POST
                添加，用户id(暂无)，用户邮箱，书籍id，书籍数量
                拿到前端数据，根据邮箱去查找记录，没有就添加，有就进行判断id有没有，没有就添加，有就修改nums
            GET
                获取，返回购物车信息
    :return:
    """
    car_db = mongo.db.car
    dic = Tool.verify_token(request.headers.get("Token"))
    mail = dic["mail"]
    if request.method == "POST":
        params = request.form
        bid = params.get("bid")
        title = params.get("title")
        nums = params.get("nums")
        if not mail or not bid or not nums:
            return {"code": 401, "msg": "缺失参数"}

        obj = {"mail": mail, "cars": [{"id": bid, "title": title, "nums": nums, "success": True}]}
        if car_db.count() == 0:
            car_db.insert_one(obj)
        else:
            result = car_db.find({"mail": mail})
            if result:
                for i in result:
                    item = i.get("cars")
                    for j in item:
                        if j.get("id") == bid:
                            car_db.update({"$and": [{"mail": mail}, {"cars.id": bid}]},
                                          {"$set": {"cars.$[].nums": int(j.get("nums")) + int(nums)}})
                        else:
                            """
                                $addToSet用于添加到数组。要将新属性添加到现有嵌入式对象中，您需要使用$set运算符和点表示法：
                                db.collection.update({name: 'a name'}, {$set: {'links.' + toType: to_link}})
                            """
                            car_db.update({"mail": mail},  {"$addToSet": {"cars": {"id": bid, "nums": nums, "success": True}}})
            else:
                car_db.insert_one(obj)
        return {"code": 200, "msg": "操作成功"}
    elif request.method == "GET":
        res = car_db.aggregate([{'$match': {'mail': mail}}, {"$unwind": "$cars"}, {"$match": {'cars.success': True}}])
        data = []
        if res:
            for i in res:
                item = i.get("cars")
                obj = {"id": item.get("id"), "nums": item.get("nums"), "title": item.get("title")}
                data.append(obj)
            return {"code": 200, "data": data}


@mall.route("/order/", methods=["GET", "POST"])
@login_required
def order():
    """
    测试接口
        订单
            获取书籍id和数量，通过书籍id去商品表查询数据
    :return:
    """
    order_db = mongo.db.order
    dic = Tool.verify_token(request.headers.get("Token"))
    mail = dic.get("mail")
    if request.method == "POST":
        params = request.form
        info = params.get("info")  # bid,bid
        remark = params.get("remark")
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        order_id = str(time + mail + "%04d" % random.randint(0, 9999)).replace(".", "")
        if not info or not order_id:
            return {"code": 401, "msg": "缺失参数"}
        car_db = mongo.db.car
        res = car_db.find({'mail': mail})
        user_cars = []
        for i in res:
            user_cars = i.get("cars")
        result = []
        for i in user_cars:
            if i.get("success") and i.get("success"):
                for j in info.split(","):
                    if i.get("id") == j:
                        result.append(i)
        book_db = mongo.db.book
        id_data = [i.get("id") for i in result]
        res = book_db.find({"id": {"$in": id_data}})
        total_data = []
        for i in res:
            for j in result:
                if i.get("id") == j.get("id"):
                    total_data.append({"id": i.get("id"), "price": i.get("price"), "nums": j.get("nums")})
        total = 0
        for i in total_data:
            total += float(i.get("price")) * int(i.get("nums"))
        obj = {"oid": order_id, "mail": mail, "time": time, "success": True, "total": total, "remark": remark}
        order_db.insert(obj)
        return {"code": 200, "msg": "操作成功"}
    else:
        # {"success": True}
        res = order_db.find({"$and": [{"mail": mail}]})
        data = []
        for i in res:
            data.append({"time": i.get("time"), "success": i.get("success"), "total": i.get("total"),
                         "remark": i.get("remark"), "mail": i.get("mail"), "oid": i.get("oid")})
        return {"code": 200, "data": data}


@mall.route("/pay/", methods=["POST"])
@login_required
def pay():
    if request.method == "POST":
        params = request.form
        oid = params.get("oid")
        if not oid:
            return {"code": 401, "msg": "参数错误"}
        order_db = mongo.db.order
        dic = Tool.verify_token(request.headers.get("Token"))
        mail = dic.get("mail")
        order_db.update({"$and": [{"mail": mail}, {"oid": oid}]}, {"$set": {"success": False}})
        return {"code": 200, "msg": "操作成功"}


@mall.route("/home/")
def home():
    """
    轮播图
    :return:
    """
    swiper_data = [{"good_id": 1, "title": "Redmi k50", "price": 1799, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/39bb34167f6c178d6bb768d8872c97f8.jpg?w=2452&h=920"},
                   {"good_id": 2, "title": "Window 11", "price": 1509, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/918820682e4a490221cfd92b24c14b86.jpg?thumb=1&w=920&h=345&f=webp&q=90"},
                   {"good_id": 3, "title": "小米12 pro", "price": 4699, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/dd741adcce9417d72ea4c1a6dfcc96e2.jpg?thumb=1&w=920&h=345&f=webp&q=90"},
                   {"good_id": 4, "title": "指尖木马", "price": 28, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/222d6c61df75f30e6782ec476d5c8273.jpg?thumb=1&w=920&h=345&f=webp&q=90"}]

    floor_data = [{"good_id": 5, "name": "mi12pro", "title": "Xiaomi 12 Pro", "price": 4699, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/02ac31f8d3848f71617e074e8e50879e.png?thumb=1&w=120&h=83&f=webp&q=90"},
                  {"good_id": 6, "name": "mi12", "title": "Xiaomi 12", "price": 3699, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/34eec49ce46adcd4739e60a2b56062fc.png?thumb=1&w=120&h=83&f=webp&q=90"},
                  {"good_id": 7, "name": "mi12x", "title": "Xiaomi x", "price": 2699, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/075d45f17b32b39c98be850a5592bbee.png?thumb=1&w=120&h=83&f=webp&q=90"},
                  {"good_id": 8, "name": "mi11le-5g-ne", "title": "小米11青春活力版", "price": 1999, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/fea69fb5990da9dfc909aa8279aaea7e.png?thumb=1&w=120&h=83&f=webp&q=90"},
                  {"good_id": 9, "name": "xiaomicivi", "title": "Xiaomi Civi", "price": 2299, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/8cad77bda138fd94eadbc2ddfced7c56.png?thumb=1&w=120&h=83&f=webp&q=90"},
                  {"good_id": 10, "name": "mix4", "title": "小米X4", "price": 4199, "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/087c52d253d9301dff7743d6bf2d0330.png?thumb=1&w=120&h=83&f=webp&q=90"}]

    category_data = [{"title": "手机", "list": floor_data},
                     {"title": "电视", "list": [{}]},
                     {"title": "笔记本\t平板", "list": [{"good_id": 11, "product_id": 10000361, "title": "小米笔记本 Pro 14 锐龙版", "image": "https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/ac38f4abb13391b5f254cd47aebb55bb.png?thumb=1&w=40&h=40&f=webp&q=90"}]},
                     {"title": "家电", "list": [{}]},
                     {"title": "出行\t穿戴", "list": [{}]},
                     {"title": "智能\t路由器", "list": [{}]},
                     {"title": "电源\t配件", "list": [{}]},
                     {"title": "健康\t儿童", "list": [{}]},
                     {"title": "音响\t耳机", "list": [{}]},
                     {"title": "生活\t箱包", "list": [{}]}]

    return {"code": 200, "data": {"swiper_data": swiper_data, "floor_data": floor_data, "category_data": category_data}}
