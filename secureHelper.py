import jwt
from hashlib import sha256
from datetime import datetime, timedelta, timezone

class JWTHelper:
    """
    jwt helper class
    """
    secret_key: str
    exp: int

    def __init__(self, data: dict):
        """
        init jwt helper class
        :param data: 'exp':seconds 'secret_key':string
        """
        # self.userid = data['id']
        self.exp = data['exp']
        self.secret_key = data['secret_key']

    def create_token(self, payload_data:dict):
        """
        create jwt token
        :param payload_data:
        :return: the jwt token
        """
        payload_data['exp'] = datetime.now(timezone.utc) + timedelta(seconds=self.exp)
        # payload_data['user_id'] = self.userid
        token = jwt.encode(payload_data, self.secret_key, algorithm='HS256')
        return token

    def decode_token(self, token:str):
        """
        decode jwt token
        :param token: jwt token
        :return: payload data
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload

        except jwt.ExpiredSignatureError:
            return "jwt.ExpiredSignatureError"
        except jwt.InvalidTokenError:
            return "jwt.InvalidTokenError"
        # except:
        #     return False

class PayloadHelper:
    """
    create payload_data string
    payload need resource_name and operation
    """
    def __init__(self, data: dict):
        """
        init payload helper class
        :param data: 'resource_id':int 'operation':str 'other_data':str
        """
        self.resource_id = data['resource_id']
        self.operation = data['operation']
        self.other_data = data['other_data']

    def create_payload(self):
        payload_data = {'resource_id': self.resource_id, 'operation': self.operation, 'other_data': self.other_data}
        return payload_data


def hash_salted_password(password: str, salt: str) -> str:
    """
    计算加盐密码的SHA256哈希值

    Args:
        password: 原始密码字符串
        salt: 盐值字符串

    Returns:
        哈希值的十六进制字符串
    """
    return sha256((salt + password).encode('utf-8')).hexdigest()

