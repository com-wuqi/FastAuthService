
"""
处理resource访问，handleResource模块用于处理具体资源
"""
"""
参见 class PayloadHelper，
根据用户id, secret_key , permission_level, 检查 ResourcePermission 表
用户是否对特定资源有对应操作的权限
然后根据 permission_level other_data(token中解码）完成操作
注意，解码 token 时仅需要校验 secret_key ，需要判断是否为该用户的key
较难完成！
"""