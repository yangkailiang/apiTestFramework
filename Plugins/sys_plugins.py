import sys
import time
from io import StringIO

from pymysql import connect
from pymysql.cursors import DictCursor
from Common import logger
from Common.utils import exception_handler
from Core.model.controller import Assertion


def restore_standard_output(*args, **kwargs):
    sys.stdout = sys.__stdout__


@exception_handler(message='执行SQLb报错：{sqlText}', throw_exception=RuntimeError)
def execute_sql_plugin(case, sqlText, name, db):
    logger.info(f"执行SQL: {sqlText}， DB: {db}, name:{name}")
    if case.env.db.get(db) is None:
        raise RuntimeError(f"未知的数据库: {db}")
    sqlText = case.render(sqlText)

    conn = connect(charset='utf8', cursorclass=DictCursor, **case.env.db[db].model_dump())
    with conn.cursor() as cursor:
        try:
            line = cursor.execute(sqlText)
            logger.info('SQL执行成功 [ROW:{}] {}'.format(line, sqlText))
        except:
            conn.rollback()
            raise RuntimeError(f"SQL执行失败：{sqlText}")

        if name:
            data = cursor.fetchall()
            if data and len(data) == 1:
                data = data[0]
            case.run_params[name] = data


@exception_handler(message='执行脚本报错Script：{script}', standby_func=restore_standard_output, throw_exception=RuntimeError)
def execute_script_plugin(case, script):
    logger.info("执行脚本")
    # 创建一个新的输出流来捕获print输出
    captured_output = StringIO()
    sys.stdout = captured_output

    def sys_set(name, val):
        case.params[name] = val
        logger.info(f"脚本设置参数成功: {name}:{val}")

    def sys_get(name):
        result = case.params.get(name)
        if not result:
            raise RuntimeError("不存在的公共参数或关联变量: {}".format(name))
        logger.info(f"脚本获取公共参数成功: {name}:{result}")
        return result

    local_vars = {
        "params": case.params, 'logger': logger, 'sys_set': sys_set, 'sys_get': sys_get, 'case': case,
    }
    exec(script, {}, local_vars)
    sys.stdout = sys.__stdout__
    stdout = captured_output.getvalue()
    if stdout:
        logger.info(f"脚本输出：{stdout}")


def sleep_plugin(case, second):
    logger.info(f"强制延时：{second}")
    time.sleep(int(second))


def add_assertion_plugin(case, expression, expect, **kwargs):
    assertion = Assertion(expression=expression, expect=expect, **kwargs)
    case.api.assertions.append(assertion)
    logger.info(f"插件添加断言成功：表达式: {expression} 预期结果：{expect}, 提取方法：{assertion.method} 断言方式：{assertion.assertion}")

