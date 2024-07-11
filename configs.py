import os

from Core.model.environment import EnvironmentStructural

# 文件目录配置

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CASE_DIR = os.path.join(BASE_DIR, 'Case')
ALLURE_REPORT_DIR = os.path.join(BASE_DIR, 'allure_result')
# 日志配置


# 默认值配置
PROTOCOL_DEFAULT = "HTTP"  # 默认协议
EXTRACT_METHOD_DEFAULT = "jinja"  # 默认提取方法
TZP_DEFAULT = 'mysql'  # 数据库类型
ENV_DEFAULT = 'test'  # 默认执行环境

HTTP_REQUEST_METHOD_DEFAULT = "POST"  # 默认请求方法
HTTP_REQUEST_TYPE_DEFAULT = "json"  # 默认请求类型
HTTP_RESPONSE_TYPE_DEFAULT = "json"  # 默认响应类型

ASSERTION_METHOD_DEFAULT = "equal"  # 默认断言方法

# 环境配置参数配置，考虑到一套自动化代码要在多个环境执行，故增加此配置
ENVS = {
    "test": {
        "domain": "https://www.tempos.cn",
        "db": {
            'test': {
                'host': 'host',
                'port': 3306,
                'user': 'user',
                'passwd': 'passwd',

            }
        },
        "redis": {
            "test": {
                "host": "127.0.1",
                "prot": 6379
            }
        },
        "server": {
            "test": {
                "hostname": "hostname",
                "port": 22,
                "username": "username",
                "password": "password"
            }
        },
    },

}

PLUGINS = {
    "sql": {
        "module": "Plugins.sys_plugins",
        "func": "execute_sql_plugin",
    },
    "script": {
        "module": "Plugins.sys_plugins",
        "func": "execute_script_plugin",
    },
    "sleep": {
        "module": "Plugins.sys_plugins",
        "func": "sleep_plugin",
    },

    "codeAssertAppend": {
        "module": "Plugins.sys_plugins",
        "func": "add_assertion_plugin",
        "auto": True,  # 是否自动执行
        "when": "afterRequest",  # 执行时间
        "value": {"expression": "{{resBody.code}}", "expect": "0000"},  # 执行参数
    },
}
