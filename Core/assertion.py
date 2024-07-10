# -*- coding: utf-8 -*-
import pytest_check

from Common.utils import str_to_list, str_to_bool, str_to_dict, str_to_num, to_str, exception_handler

ASSERT_MAP = {
    ("equal", "equals", "相等", "字符相等"): {'func': pytest_check.equal, 'desc': '实际值({}) 等于 预期值({})：', 'handle_result': str},
    ("equalsList", "数组相等"): {'func': pytest_check.equal, 'desc': '数组相等', 'handle_result': str_to_list},
    ("equalsDict", "对象相等"): {'func': pytest_check.equal, 'desc': '对象相等', 'handle_result': str_to_dict},
    ("equalsNumber", "数字相等", "数值相等"): {'func': pytest_check.equal, 'desc': '数值相等', 'handle_result': str_to_list},
    # ("equalIgnoreCase", "相等(忽略大小写)"): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    ("notEqual", "does not equal", "不等于"): {'func': pytest_check.not_equal, 'desc': '不等于', },
    ("contains", "包含"): {'func': pytest_check.is_in, 'desc': '包含', 'handle_result': to_str},
    ("isTrue", ): {'func': pytest_check.is_true, 'desc': '为True', 'handle_result': str_to_bool, 'only_actual': True},

    # pytest_check.
    # ("notContains", "does no contains", "不包含"): {'func': 'pytest_check.is_not_in', 'desc': '不包含', 'handle_result': ''},
    # ("containsOnly", "仅包含"): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    # (): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    # (): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    # (): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    # (): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},
    # (): {'func': 'pytest_check.equal', 'desc': '', 'handle_result': ''},

}


@exception_handler(message='断言出错：Assertion:{assertion}, Actual: {actual}, Expect: {expect}', throw_exception=RuntimeError)
def compare(assertion, actual, expect=True):
    for key, value in ASSERT_MAP.items():
        if assertion in key:
            handle_result = value.get('handle_result')
            if handle_result:
                actual = handle_result(actual)
                expect = handle_result(expect)
            if value.get('only_actual') is True:
                is_success = value['func'](actual)
            else:
                is_success = value['func'](actual, expect)
            message = value['desc'].format(actual, expect)
            return is_success, message
    return False, "未知的断言类型"
