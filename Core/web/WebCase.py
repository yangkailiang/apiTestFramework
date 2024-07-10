from collections import ChainMap

from Common.utils import exception_handler
from Common import logger
from Common.template import template_object
from Core.model.web_struct import WebOperationStructural
from Core.web.driver.find_opt import OPERATIONS_MAP, operation_instance
from Core.mapping import PARAMS
from Core.model.reslut_struct import ApiResultStructural


class WebCase:
    def __init__(self, opt: dict, public_params, params, result: ApiResultStructural):
        self.opt = WebOperationStructural(**opt)
        self.operationId = self.opt.operationId
        self.public_params = public_params
        self.params = ChainMap(params, public_params)
        self.result = result

    @exception_handler(message='处理步骤参数报错', throw_exception=RuntimeError)
    def handel_operation_data(self):
        """ 处理步骤参数报错 """
        for name, expr in self.opt.operationData.items():
            self.opt.operationData[name] = template_object.render(
                string=PARAMS.get(expr['type'], lambda value: value)(expr['value']),
                source=self.params
            )

    @exception_handler(message='执行条件判断操作报错', throw_exception=RuntimeError)
    def condition(self, func, element: dict) -> list:
        """ 执行条件判断操作 """
        true, false = self.opt.operationData.pop('true', ''), self.opt.operationData.pop('false', '')
        success, message = func(**self.opt.operationData, **element)
        if success is True:
            logger.info(f"判断成功, 执行判断成功步骤: {true}", extra={'identification': f"operationId:{self.operationId}"})
            return true.split(',')

        logger.info(f"判断失败, 执行判断失败步骤: {false}", extra={'identification': f"operationId:{self.operationId}"})
        return false.split(',')

    def main(self):
        try:
            operation_instance.operationId = self.operationId
            self.handel_operation_data()
            element = self.opt.operationElement.get('element', dict())
            func = OPERATIONS_MAP[self.opt.operationType][self.opt.operationTrans]

            if self.opt.operationTrans == "屏幕截图":
                self.opt.operationData['result'] = self.result

            self.result.description = self.opt.operationDesc
            self.result.content = element.get('target', '')

            if func is None:
                raise RuntimeError(f"未知的操作类型: {self.opt.operationTrans}")
            if self.opt.operationType == "condition":
                return self.condition(func=func, element=element)
            func(**self.opt.operationData, **element)
        except:
            operation_instance.operationId = ''
            raise RuntimeError(f"执行报错: {self.opt}")
