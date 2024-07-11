import ast
import os
from urllib.parse import quote
from json import dumps
from yaml import dump, load, FullLoader

import json
import re
import jsonpath

from traceback import format_exc


def custom_format(input_string, dictionary):
    def replacement(match):
        var_name = match.group(1)
        return dictionary.get(var_name, "{%s}" % var_name)

    return re.sub(r'\{(\w+)\}', replacement, input_string)


def exception_handler(message=None, standby_func=None, capture_exception=Exception, throw_exception=None):
    """
    捕获（capture_exception）指定错误后，抛出（throw_exception）指定错误，可选择报错后执行函数，函数会传入和被装饰函数相同的参数
    :param message: 抛出异常时的msg，会自动拼接异常信息，可以用 {key} 来提取请求参数，注意再调用装饰函数时只有关键字参数才可提取
    :param standby_func: 报错后执行的函数，需要接收参数：被装饰函数的全部入参，为none时不执行
    :param capture_exception: 捕获的错误
    :param throw_exception: 抛出的错误，为none时不报错
    :return: 被装饰函数执行结果
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except capture_exception as e:
                try:
                    msg = custom_format(message, kwargs) if message is not None else ''
                except:
                    msg = message
                if standby_func is not None:
                    standby_func(*args, **kwargs, message=f"{msg}\nError: {format_exc()}")
                if throw_exception is not None:
                    raise throw_exception(f"{msg}\nError:{e}")

        return wrapper

    return decorator


# 写入yaml文件
def write_yaml(data, path, mode='w'):
    with open(path, mode=mode, encoding='utf-8') as f:
        dump(data, stream=f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return data


# 读取yaml文件
def read_yaml(path, key=None):
    with open(path, 'r', encoding='utf-8') as f:
        data = load(f, Loader=FullLoader)
        if key:
            return data.get(key) if data else data
        return {} if not data else data


# 字符串转换为bool类型
def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if not value:
        return None
    result = value.lower()
    if result == 'true':
        return True

    elif result == 'false':
        return False
    else:
        raise ValueError(f"{value}: 转换Bool类型失败")


def str_to_none(value):
    """ 字符串转 None"""
    if str(value).lower() in ('none', 'null'):
        return None
    else:
        raise ValueError(f"{value}: 转换None类型失败")


def str_to_num(value):
    if isinstance(value, int | float):
        return value
    if not value:
        return 0
    if isinstance(value, str):
        if '.' in value:
            return float(value)
        else:
            return int(value)
    else:
        raise ValueError(f"{value}: 转换数字类型失败")


def str_to_list(value) -> list:
    if not value:
        return list()
    if isinstance(value, list):
        return value
    if isinstance(value, int | float):
        return [value, ]

    if isinstance(value, str):
        result = ast.literal_eval(value)
        if isinstance(result, list):
            return result
        else:
            raise ValueError(f"{value}: 转换数组类型失败: {result}")
    else:
        raise ValueError(f"{value}: 转换数组类型失败")


def str_to_dict(value):
    if isinstance(value, dict | int | float):
        return value

    elif not value:
        return None
    elif isinstance(value, str):
        result = ast.literal_eval(value)
        if isinstance(result, dict):
            return result
        else:
            raise ValueError(f"{value}: 转换字典类型失败: {result}")
    else:
        raise ValueError(f"{value}: 转换字典类型失败")


def to_str(value):
    if isinstance(value, int | float):
        return value
    elif not value:
        return ""
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def list_len(value):
    return len(str_to_list(value))


def proxies_join(proxies: dict):
    if 'url' not in proxies or proxies['url'] is None or len(proxies['url']) == 0:
        raise ProxiesError("未设置代理网址")
    if not proxies['url'].startswith('http'):
        proxies['url'] = 'http://' + proxies['url']
    if 'username' not in proxies or proxies['username'] is None or len(proxies['username']) == 0:
        proxies['username'] = None
    else:
        proxies['username'] = quote(proxies['username'], safe='')
    if 'password' not in proxies or proxies['password'] is None or len(proxies['password']) == 0:
        proxies['password'] = None
    else:
        proxies['password'] = quote(proxies['password'], safe='')
    scheme = proxies['url'].split(':')[0]
    if proxies['username'] is not None and proxies['password'] is not None:
        pre, suf = proxies['url'].split('//', maxsplit=1)
        url = '{}//{}:{}@{}'.format(pre, proxies['username'], proxies['password'], suf)
        return {scheme: url}
    elif proxies['username'] is None and proxies['password'] is None:
        return {scheme: proxies['url']}
    else:
        raise ProxiesError("未设置代理账号或密码")


def custom_dumps(data):
    try:
        return dumps(data, indent=4, ensure_ascii=False)
    except:
        return data


class ProxiesError(Exception):
    """错误代理"""


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
