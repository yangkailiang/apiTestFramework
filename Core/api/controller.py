import importlib
import sys

from Common import logger
from Common.exceptions import ConditionNotEstablished
from Common.utils import exception_handler
# from Core.api.httpApi import HttpApiTestCase

from Core.assertion import compare
from Core.utils import extract_by_jsonpath, extract_by_regex

from configs import PLUGINS


class DynamicImporter:
    def __init__(self, module_name):
        self.module_name = module_name

    def __enter__(self) -> list:
        # 在进入上下文时导入模块
        try:

            return importlib.import_module(self.module_name)
        except Exception as e:
            raise RuntimeError(f"导包出错{self.module_name}: {str(e)}")

    def __exit__(self, exc_type, exc_value, traceback):
        # 在离开上下文时进行清理
        if self.module_name in sys.modules:
            del sys.modules[self.module_name]


class ApiController:
    """逻辑判断"""

    @exception_handler(message="逻辑判断失败，跳过执行", throw_exception=ConditionNotEstablished)
    def execute_whetherExec(self, whetherExec):
        """ 处理并执行 whetherExec，如果条件不成立，则抛出异常"""
        if not whetherExec:
            return
        for condition in whetherExec:
            target = self.render(condition.target)
            success, message = compare(assertion=condition.assertion, actual=target, expect=condition.expect)
            logger.info(f"条件判断: {message}, 是否成立：{success}")
            if success is False:
                raise ConditionNotEstablished("条件不成立，跳过执行")

    @exception_handler(message="执行操作出错：", throw_exception=RuntimeError)
    def execute_plugin(self, opts):
        if not opts:
            return
        for opt in opts:
            if not PLUGINS.get(opt.name):
                raise RuntimeError(f"未知的插件: {opt.name}")
            plugin = PLUGINS[opt.name]
            with DynamicImporter(plugin["module"]) as module:
                if isinstance(opt.value, dict):
                    getattr(module, plugin["func"])(case=self, **opt.value)

                elif isinstance(opt.value, list):
                    getattr(module, plugin["func"])(case=self, *opt.value)
                else:
                    getattr(module, plugin["func"])(self, opt.value)

    def extract(self, name: str, expression: str):
        if name == 'jsonpath':
            return extract_by_jsonpath(data=self.params, expression=expression)
        elif name == 're':
            return extract_by_regex(data=self.params, pattern=expression)
        elif name == "jinja":
            return self.render(expression)
        else:
            raise RuntimeError("未定义提取函数: {}".format(name))

    def execute_assertion(self, assertions, errorContinue):
        """ 执行断言 """
        if not assertions:
            return

        for assertion in assertions:
            result = self.extract(name=assertion.method, expression=assertion.expression)
            success, message = compare(assertion=assertion.assertion, actual=result, expect=assertion.expect)
            logger.info(f"断言：{message}, 断言结果：{success}")

            if success is False and errorContinue is False:
                raise AssertionError(f"{message}，断言失败，中断执行")

    @exception_handler(message="提取关联参数失败：", throw_exception=RuntimeError)
    def extract_relation_params(self, relations):
        """ 提取关联参数 """
        if not relations:
            return None
        relations_result = {}
        for relation in relations:
            result = self.extract(
                name=relation.method,
                expression=relation.expression
            )
            relations_result[relation.name] = result
            logger.info(f"关联参数提取成功，取值函数：{relation.method}，变量名:{relation.name}，提取结果:{result}")
        self.relation_params.update(relations_result)
        return relations_result
