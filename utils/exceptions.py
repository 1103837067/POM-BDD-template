class TestFrameworkException(Exception):
    """测试框架基础异常类"""
    pass

class ElementException(TestFrameworkException):
    """元素操作相关异常"""
    pass

class ConfigurationError(TestFrameworkException):
    """配置相关错误"""
    pass

class TestDataError(TestFrameworkException):
    """测试数据相关错误"""
    pass

class BrowserException(TestFrameworkException):
    """浏览器操作相关异常"""
    pass

class ValidationError(TestFrameworkException):
    """验证失败异常"""
    pass

class TimeoutException(TestFrameworkException):
    """超时异常"""
    pass

class NetworkException(TestFrameworkException):
    """网络相关异常"""
    pass 