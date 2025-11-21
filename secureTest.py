import unittest
from secureHelper import *

class MainTestCase(unittest.TestCase):

    def setUp(self):
        # 在每个测试前设置数据
        data_jwt = {"exp": 120, "secret_key": "test_key"}
        self.jwt_tool = JWTHelper(data_jwt)
        data_payload = {'resource_id': 0, 'operation': "test", 'other_data': "test_1"}
        self.payload_test = PayloadHelper(data_payload)

    def test_token_creation_and_decoding(self):
        """测试token创建和解码功能"""
        payload_data = self.payload_test.create_payload()
        token = self.jwt_tool.create_token(payload_data)

        # 解码token
        decoded_payload = self.jwt_tool.decode_token(token)

        self.assertEqual(decoded_payload['resource_id'], 0)
        self.assertEqual(decoded_payload['operation'], "test")
        self.assertEqual(decoded_payload['other_data'], "test_1")

        # 验证token是字符串类型
        self.assertIsInstance(token, str)

        # 验证解码后的payload是字典类型
        self.assertIsInstance(decoded_payload, dict)

    def test_expired_token(self):
        """测试过期token的处理"""
        # 创建立即过期的token
        data_jwt_expired = {"exp": -10, "secret_key": "test_key"}  # 负的过期时间
        jwt_tool_expired = JWTHelper(data_jwt_expired)

        payload_data = self.payload_test.create_payload()
        token = jwt_tool_expired.create_token(payload_data)

        result = jwt_tool_expired.decode_token(token)
        self.assertEqual(result, "jwt.ExpiredSignatureError")

    def test_invalid_token(self):
        """测试无效token的处理"""
        invalid_token = "invalid.token.here"
        result = self.jwt_tool.decode_token(invalid_token)
        self.assertEqual(result, "jwt.InvalidTokenError")


if __name__ == '__main__':
    unittest.main()
