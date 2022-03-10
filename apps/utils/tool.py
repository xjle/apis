import random
import bcrypt
from bson import ObjectId, json_util
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Tool:
    def __init__(self):
        pass

    @staticmethod
    def get_verification(num=6, alpha=True):
        """
        随机生成验证码
        :param num:
        :param alpha:
        :return:
        """
        code_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if alpha:  # 是否需要携带字母
            for i in range(65, 91):
                code_list.append(chr(i))
            for i in range(97, 123):
                code_list.append(chr(i))
        code = ''.join(random.sample(code_list, num))
        return code

    @staticmethod
    def encryption(value):
        """
        加密
        :param value:
        :return:
        """
        res = value.encode('utf-8')
        ret = bcrypt.hashpw(res, bcrypt.gensalt())
        return ret

    @staticmethod
    def decrypt(value, hash_pwd):
        """
        解密
        :param value:
        :param hash_pwd:
        :return:
        """
        ret = bcrypt.checkpw(value.encode('utf-8'), hash_pwd.encode('utf-8'))
        return ret

    @staticmethod
    def create_token(args):
        s = Serializer(current_app.config.get('SECRET_KEY'),
                       expires_in=current_app.config.get('PERMANENT_SESSION_LIFETIME'))
        # 接收用户id转换与编码
        token = s.dumps({'id': str(args.get("id")), 'mail': args.get('mail'), 'role': args.get('role')}).decode('ascii')
        return token

    @staticmethod
    def verify_token(token):
        """
        :param token:
        :return:
        """
        # 参数为私有秘钥，跟上面方法的秘钥保持一致
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            # 转换为字典
            data = s.loads(token)
            return data
        except Exception:
            return None
