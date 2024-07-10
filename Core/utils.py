import json
import re
import jsonpath

from pydantic import ValidationError

from Common.utils import exception_handler
from Core.model.fields import fields


@exception_handler(message="拼接URL失败：Domain: {domain}, Path: {path}", throw_exception=RuntimeError)
def url_join(domain, path):
    domain = domain[:-1] if domain.endswith('/') else domain
    path = path[1:] if path.startswith('/') else path
    return f"{domain}/{path}"


@exception_handler(message="jsonpath提取失败：Expression: {expression}, dData: {data}", throw_exception=RuntimeError)
def extract_by_jsonpath(data: dict | str, expression: str):
    """
    jsonpath 提取器
    :param data: 数据源
    :param expression: 表达式
    :return:
    """
    if not isinstance(data, dict):
        raise RuntimeError('被提取的值不是json, 不支持jsonpath')

    value = jsonpath.jsonpath(data, expression)
    if value:
        return value[0] if len(value) == 1 else value
    else:
        raise RuntimeError('jsonpath表达式错误: {}'.format(expression))


# 正则提取
@exception_handler(message="正则提取失败：Pattern: {pattern}, dData: {data}", throw_exception=RuntimeError)
def extract_by_regex(data: dict | str, pattern: str):
    """
    正则提取器
    :param data: 数据源
    :param pattern: 表达式
    :return:
    """
    if isinstance(data, dict):
        content = json.dumps(data, ensure_ascii=False)
    else:
        content = data
    result = re.findall(pattern, content)
    if len(result) > 0:
        return result[0] if len(result) == 1 else result
    else:
        raise RuntimeError("正则表达式匹配失败: {}".format(pattern))


def handel_ValidationError(errors: ValidationError):
    """
    处理结构体报错 ValidationError
    :param errors: 捕获的报错： ValidationError
    :return:
    """
    if not isinstance(errors, ValidationError):
        raise RuntimeError("处理结构体报错，传入的报错类型错误")
    output = []
    for error in errors.errors():
        loc = (i for i in error["loc"] if isinstance(i, str))
        loc = '.'.join(loc)
        output.append(f'{fields.get(loc, loc)}校验失败: {error["msg"]}')
    return output


def merge_dictionary(*args):
    all_dictionary = dict()
    if args:
        for dct in args:
            if dct and isinstance(dct, dict):
                all_dictionary.update(dct)
    return all_dictionary



