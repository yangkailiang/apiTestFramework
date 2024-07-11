# -*- coding: utf-8 -*-
import pytest_check

from Common.utils import str_to_list, str_to_bool, str_to_dict, str_to_num, to_str, exception_handler

ASSERT_MAP = {
    "equal": {'func': pytest_check.equal, 'desc': '实际值({}) 等于 预期值({})：', 'handle_result': str},
    "equalsList": {'func': pytest_check.equal, 'desc': '数组相等', 'handle_result': str_to_list},
    "equalsDict": {'func': pytest_check.equal, 'desc': '对象相等', 'handle_result': str_to_dict},
    "equalsNumber": {'func': pytest_check.equal, 'desc': '数值相等', 'handle_result': str_to_list},
    "notEqual": {'func': pytest_check.not_equal, 'desc': '不等于', },
    "in": {'func': pytest_check.is_in, 'desc': '包含', 'handle_result': to_str},
    "isTrue": {'func': pytest_check.is_true, 'desc': '为True', 'handle_result': str_to_bool, 'only_actual': True},
    "notIn": {'func': 'pytest_check.is_not_in', 'desc': '不包含', 'handle_result': to_str},

}
ASSERT_MAP.update({
    "相等": ASSERT_MAP["equal"],
    "字符相等": ASSERT_MAP["equal"],
    "数组相等": ASSERT_MAP["equalsList"],
    "对象相等": ASSERT_MAP["equalsDict"],
    "数字相等": ASSERT_MAP["equalsNumber"],
    "数值相等": ASSERT_MAP["equalsNumber"],
    "不等于": ASSERT_MAP["notEqual"],
    "包含": ASSERT_MAP["in"],
    "不包含": ASSERT_MAP["notIn"],
    "为真": ASSERT_MAP["isTrue"],

})

def _compare(actual, expect, func, desc, handle_result=None, only_actual=None):
    """
    比较实际值和预期值
    :param actual: 实际值
    :param expect: 预期值
    :param func: 比较函数
    :param desc: 描述信息
    :param handle_result: 处理结果函数
    :param only_actual: 只比较实际值
    :return: 比较结果和描述信息
    """
    if handle_result:
        actual = handle_result(actual)
        expect = handle_result(expect)
    if only_actual is True:
        is_success = func(actual)
    else:
        is_success = func(actual, expect)
    message = desc.format(actual, expect)
    return is_success, message

@exception_handler(message='断言出错：Assertion:{assertion}, Actual: {actual}, Expect: {expect}', throw_exception=RuntimeError)
def compare(assertion, actual, expect=True):
    return _compare(actual=actual, expect=expect, **ASSERT_MAP[assertion])
