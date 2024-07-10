from Common.utils import exception_handler
from Common.logger import logger
from Core.web.driver import Operation, add_error_log


class Relation(Operation):
    """关联类操作"""

    @exception_handler(message='保存{title}报错', throw_exception=RuntimeError, standby_func=add_error_log)
    def save(self, name, value, title):
        if name in self.params:
            raise RuntimeError(f"Key: {name} 已存在，保存失败")
        self.params[name] = value
        logger.info(f"保存{title}成功: {value}", extra={'identification': f"operationId:{self.operationId}"})

    def save_page_title(self, save_name):
        """获取页面标题"""
        self.save(name=save_name, value=self.get_page_title(), title='页面标题')

    def save_page_url(self, save_name):
        """获取页面url"""
        self.save(name=save_name, value=self.get_page_url(), title='页面url')

    def save_ele_html(self, by, expression, target, save_name):
        self.save(name=save_name, value=self.get_ele_html(by=by, expression=expression, target=target), title='元素源码')

    def save_ele_text(self, by, expression, target, save_name):
        """获取元素文本"""
        self.save(name=save_name, value=self.get_ele_text(by=by, expression=expression, target=target), title='元素文本')

    def save_ele_tag(self, by, expression, target, save_name):
        """获取元素tag"""
        self.save(name=save_name, value=self.get_ele_tag(by=by, expression=expression, target=target), title='元素tag')

    def save_ele_size(self, by, expression, target, save_name):
        """获取元素尺寸"""
        self.save(name=save_name, value=self.get_ele_size(by=by, expression=expression, target=target), title='元素尺寸')

    def save_ele_height(self, by, expression, target, save_name):
        """获取元素高度"""
        self.save(name=save_name, value=self.get_ele_height(by=by, expression=expression, target=target), title='元素高度')

    def save_ele_width(self, by, expression, target, save_name):
        """获取元素宽度"""
        self.save(name=save_name, value=self.get_ele_width(by=by, expression=expression, target=target), title='元素宽度')

    def save_ele_location(self, by, expression, target, save_name):
        """获取元素位置"""
        self.save(name=save_name, value=self.get_ele_location(by=by, expression=expression, target=target), title='元素位置')

    def save_ele_x(self, by, expression, target, save_name):
        """获取元素X坐标"""
        self.save(name=save_name, value=self.get_ele_x(by=by, expression=expression, target=target), title='元素X坐标')

    def save_ele_y(self, by, expression, target, save_name):
        """获取元素Y坐标"""
        self.save(name=save_name, value=self.get_ele_y(by=by, expression=expression, target=target), title='元素Y坐标')

    def save_ele_attribute(self, by, expression, target, name, save_name):
        """获取元素属性"""
        self.save(name=save_name, value=self.get_ele_attribute(by=by, expression=expression, target=target, name=name), title='元素属性')

    def save_ele_css(self, by, expression, target, name, save_name):
        """获取元素css样式"""
        self.save(name=save_name, value=self.get_ele_css(by=by, expression=expression, target=target, name=name), title='元素css样式')

    def save_window_position(self, save_name):
        """获取窗口位置"""
        self.save(name=save_name, value=self.get_window_position(), title='窗口位置')

    def save_window_x(self, save_name):
        """获取窗口X坐标"""
        self.save(name=save_name, value=self.get_window_x(), title='窗口X坐标')

    def save_window_y(self, save_name):
        """获取窗口Y坐标"""
        self.save(name=save_name, value=self.get_window_y(), title='窗口Y坐标')

    def save_window_size(self, save_name):
        """获取窗口大小"""
        self.save(name=save_name, value=self.get_window_size(), title='窗口大小')

    def save_window_width(self, save_name):
        """获取窗口宽度"""
        self.save(name=save_name, value=self.get_window_width(), title='窗口宽度')

    def save_window_height(self, save_name):
        """获取窗口高度"""
        self.save(name=save_name, value=self.get_window_height(), title='窗口高度')

    def save_current_handle(self, save_name):
        """获取当前窗口句柄"""
        self.save(name=save_name, value=self.driver.current_window_handle, title='当前窗口句柄')

    def save_all_handle(self, save_name):
        """获取所有窗口句柄"""
        self.save(name=save_name, value=self.driver.window_handles, title='所有窗口句柄')

    def save_cookies(self, save_name):
        """获取cookies"""
        self.save(name=save_name, value=self.get_cookies(), title='cookies')

    def save_cookie(self, name, save_name):
        """获取cookie"""
        self.save(name=save_name, value=self.get_cookie(name=name), title='cookies')

    # def custom(self, **kwargs):
    #     """自定义"""
    #     code = kwargs["code"]
    #     names = locals()
    #     names["element"] = kwargs["element"]
    #     names["data"] = kwargs["data"]
    #     names["driver"] = self.driver
    #     names["test"] = self.test
    #     try:
    #         """关联操作需要返回被断言的值 以sys_return(value)返回"""
    #
    #         def print(*args, sep=' ', end='\n', file=None, flush=False):
    #             if file is None or file in (sys.stdout, sys.stderr):
    #                 file = names["test"].stdout_buffer
    #             self.print(*args, sep=sep, end=end, file=file, flush=flush)
    #
    #         def sys_return(res):
    #             names["_exec_result"] = res
    #
    #         def sys_get(name):
    #             if name in names["test"].context:
    #                 return names["test"].context[name]
    #             elif name in names["test"].common_params:
    #                 return names["test"].common_params[name]
    #             else:
    #                 raise KeyError("不存在的公共参数或关联变量: {}".format(name))
    #
    #         def sys_put(name, val, ps=False):
    #             if ps:
    #                 names["test"].common_params[name] = val
    #             else:
    #                 names["test"].context[name] = val
    #
    #         exec(code)
    #         self.test.debugLog("成功执行 %s" % kwargs["trans"])
    #     except NoSuchElementException as e:
    #         raise e
    #     except Exception as e:
    #         self.test.errorLog("无法执行 %s" % kwargs["trans"])
    #         raise e
    #     else:
    #         self.test.context[kwargs["data"]["save_name"]] = names["_exec_result"]
