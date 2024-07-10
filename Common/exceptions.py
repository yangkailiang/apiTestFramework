class AnalysisTaskError(Exception):
    """ 解析task错误 """


class TokenExpirationError(Exception):
    """ token 过期"""


class HttpStatusCodeError(Exception):
    """ http 状态码 不是200 """


class TypeConversionError(Exception):
    """ 类型转换错误 """


class AssertionTypeNotExist(Exception):
    """断言类型错误"""


class ConditionNotEstablished(Exception):
    """ 条件不成立，跳过执行 """


class SeriousError(Exception):
    """ 严重的报错，将会中断执行 """

