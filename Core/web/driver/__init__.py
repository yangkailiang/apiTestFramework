from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from Common.utils import exception_handler, str_to_bool
from Common import logger
from Core.assertion import compare


def add_error_log(self, message, *args, **kwargs):
    # self.report.error_log(message)
    # logger.error(message)
    pass


class Operation(object):
    def __init__(self, driver: Chrome = None, params=None):
        self.driver = driver
        self.params = params
        self.operationId = ''

    @exception_handler(message='{title}报错', throw_exception=AssertionError, standby_func=add_error_log)
    def compare(self, assertion, actual, expect, title, **kwargs):
        success, message = compare(assertion=assertion, actual=actual, expect=expect)
        if success is False:
            logger.info(f"{title}失败: {message}", extra={'identification': f"operationId:{self.operationId}"})
            isContinue = str_to_bool(kwargs.get('continue', True))
            if isContinue is False:
                raise AssertionError(message)
            return success, message
        logger.info(f"{title}成功: {message}", extra={'identification': f"operationId:{self.operationId}"})
        return success, message

    @exception_handler(message='{title}报错', throw_exception=AssertionError, standby_func=add_error_log)
    def compare_condition(self, assertion, actual, expect, title):
        success, message = compare(assertion=assertion, actual=actual, expect=expect)
        if success is False:
            logger.info(f"{title}失败: {message}", extra={'identification': f"operationId:{self.operationId}"})
            return success, message
        logger.info(f"{title}成功: {message}", extra={'identification': f"operationId:{self.operationId}"})
        return success, message

    @staticmethod
    def get_locator(locator):
        match locator.lower():
            case 'css':
                return By.CSS_SELECTOR
            case 'id':
                return By.ID
            case 'xpath':
                return By.XPATH
            case 'link':
                return By.LINK_TEXT
            case 'class_name':
                return By.CLASS_NAME
            case 'name':
                return By.NAME
            case 'tag_name':
                return By.TAG_NAME
            case _:
                raise ValueError(f'未知的选择器：【{locator}】')

    @exception_handler(message='{target} By: {by} Expression: {expression}: 定位元素失败', throw_exception=RuntimeError,
                       standby_func=add_error_log)
    def find_element(self, by, expression, target):
        """查找单个元素"""
        element_obj = self.driver.find_element(self.get_locator(by), expression)
        logger.info(f"成功定位元素:{target} By: {by} Expression: {expression}", extra={'identification': f"operationId:{self.operationId}"})
        return element_obj

    @exception_handler(message='{target} By: {by} Expression: {expression}: 定位批量元素失败', throw_exception=RuntimeError,
                       standby_func=add_error_log)
    def find_elements(self, by, expression, target):
        """查找批量元素"""
        elements_obj = self.driver.find_elements(self.get_locator(by), expression)
        if len(elements_obj) > 0:
            logger.info(f"{target}[{len(elements_obj)}] By: {by} Expression: {expression}: 成功定位元素", extra={'identification': f"operationId:{self.operationId}"})
            return elements_obj
        else:
            raise NoSuchElementException(f'{target} By: {by} Expression: {expression}: 定位批量元素失败')


    @exception_handler(message='获取页面标题失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_page_title(self):
        """获取页面标题"""
        title = self.driver.title
        logger.info(f"成功获取title:{title}", extra={'identification': f"operationId:{self.operationId}"})
        return title

    @exception_handler(message='获取页面url失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_page_url(self):
        """获取页面url"""
        url = self.driver.current_url
        logger.info(f"成功获取URL:{url}", extra={'identification': f"operationId:{self.operationId}"})
        return url

    @exception_handler(message='获取页面源码失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_page_source(self):
        """判断页面源码"""
        source = self.driver.page_source
        logger.info("成功获取page source: : 源码过长不予展示", extra={'identification': f"operationId:{self.operationId}"})
        return source

    @exception_handler(message='获取元素文本失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_text(self, by, expression, target):
        """获取元素文本"""
        text = self.find_element(by=by, expression=expression, target=target).text
        logger.info(f"获取元素文本成功{text}", extra={'identification': f"operationId:{self.operationId}"})
        return text

    @exception_handler(message='获取元素Tag失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_tag(self, by, expression, target):
        """获取元素tag"""
        tag = self.find_element(by=by, expression=expression, target=target).tag_name
        logger.info(f"获取元素Tag成功: {tag}", extra={'identification': f"operationId:{self.operationId}"})
        return tag

    @exception_handler(message='获取元素尺寸失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_size(self, by, expression, target):
        """获取元素尺寸"""
        size = self.find_element(by=by, expression=expression, target=target).size
        logger.info(f"获取元素尺寸成功: {size}", extra={'identification': f"operationId:{self.operationId}"})
        return size

    @exception_handler(message='获取元素高度失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_height(self, by, expression, target):
        """获取元素高度"""
        height = self.find_element(by=by, expression=expression, target=target).size.get("height")
        logger.info(f"获取元素高度成功: {height}", extra={'identification': f"operationId:{self.operationId}"})
        return height

    @exception_handler(message='获取元素宽度失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_width(self, by, expression, target):
        """获取元素宽度"""
        width = self.find_element(by=by, expression=expression, target=target).size.get("width")
        logger.info(f"获取元素宽度成功: {width}", extra={'identification': f"operationId:{self.operationId}"})
        return width

    @exception_handler(message='获取元素位置失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_location(self, by, expression, target):
        """获取元素位置"""
        location = self.find_element(by=by, expression=expression, target=target).location
        logger.info(f"获取元素位置成功: {location}", extra={'identification': f"operationId:{self.operationId}"})
        return location

    @exception_handler(message='获取元素X坐标失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_x(self, by, expression, target):
        """获取元素X坐标"""
        x = self.find_element(by=by, expression=expression, target=target).location.get("x")
        logger.info(f"获取元素X坐标成功: {x}", extra={'identification': f"operationId:{self.operationId}"})
        return x

    @exception_handler(message='获取元素Y坐标失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_y(self, by, expression, target):
        """获取元素Y坐标"""
        y = self.find_element(by=by, expression=expression, target=target).location.get("y")
        logger.info(f"获取元素Y坐标成功: {y}", extra={'identification': f"operationId:{self.operationId}"})
        return y

    @exception_handler(message='获取元素html成功失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_html(self, by, expression, target):
        """获取元素属性"""
        outerHTML = self.find_element(by=by, expression=expression, target=target).get_attribute("outerHTML")
        logger.info(f"获取元素html成功: {outerHTML}", extra={'identification': f"operationId:{self.operationId}"})
        return outerHTML

    @exception_handler(message='获取元素属性失败: Name: {name}', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_attribute(self, by, expression, target, name):
        """获取元素属性"""
        attribute = self.find_element(by=by, expression=expression, target=target).get_attribute(name)
        logger.info(f"获取元素属性成功 Name: {name}  Attribute: {attribute}", extra={'identification': f"operationId:{self.operationId}"})
        return attribute

    @exception_handler(message='获取元素css样式失败: Name: {name}', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_css(self, by, expression, target, name):
        """获取元素css样式"""
        css = self.find_element(by=by, expression=expression, target=target).value_of_css_property(name)
        logger.info(f"获取元素css样式成功 Name: {name}  Result: {css}", extra={'identification': f"operationId:{self.operationId}"})
        return css

    @exception_handler(message='获取窗口位置失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_position(self):
        """获取窗口位置"""
        position = self.driver.get_window_position()
        logger.info(f"获取窗口位置成功 {position}", extra={'identification': f"operationId:{self.operationId}"})
        return position

    @exception_handler(message='获取窗口X坐标失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_x(self):
        """获取窗口X坐标"""
        x = self.driver.get_window_position().get("x")
        logger.info(f"获取窗口X坐标成功: {x}", extra={'identification': f"operationId:{self.operationId}"})
        return x

    @exception_handler(message='获取窗口Y坐标失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_y(self):
        """获取窗口Y坐标"""
        y = self.driver.get_window_position().get("y")
        logger.info(f"获取窗口Y坐标成功: {y}", extra={'identification': f"operationId:{self.operationId}"})
        return y

    @exception_handler(message='获取窗口大小失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_size(self):
        """获取窗口大小"""
        size = self.driver.get_window_size()
        logger.info(f"获取窗口大小成功: {size}", extra={'identification': f"operationId:{self.operationId}"})
        return size

    @exception_handler(message='获取窗口宽度失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_width(self):
        """获取窗口宽度"""
        width = self.driver.get_window_size().get("width")
        logger.info(f"获取窗口宽度成功: {width}", extra={'identification': f"operationId:{self.operationId}"})
        return width

    @exception_handler(message='获取窗口高度失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_window_height(self):
        """获取窗口高度"""
        height = self.driver.get_window_size().get("height")
        logger.info(f"获取窗口高度成功: {height}", extra={'identification': f"operationId:{self.operationId}"})
        return height

    @exception_handler(message='获取当前窗口句柄失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_current_handle(self):
        """获取当前窗口句柄"""
        handle = self.driver.current_window_handle
        logger.info(f"获取当前窗口句柄成功: {str(handle)}")
        return handle

    @exception_handler(message='获取所有窗口句柄失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_all_handle(self):
        """获取所有窗口句柄"""
        window_handles = self.driver.window_handles
        logger.info(f"获取所有窗口句柄成功: {str(window_handles)}", extra={'identification': f"operationId:{self.operationId}"})
        return window_handles

    @exception_handler(message='获取所有Cookies失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_cookies(self):
        """获取cookies"""
        cookies = self.driver.get_cookies()
        logger.info(f"获取所有Cookie成功: {str(cookies)}", extra={'identification': f"operationId:{self.operationId}"})
        return cookies

    @exception_handler(message='获取指定cookie失败: Name: {name}', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_cookie(self, name):
        """获取cookie"""
        cookie = self.driver.get_cookie(name)
        logger.info(f"获取指定cookie成功: Name: {name}, Cookie: {cookie}", extra={'identification': f"operationId:{self.operationId}"})
        return cookie

    @exception_handler(message='获取元素是否选中失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_selected(self, by, expression, target):
        """获取元素是否选中"""
        is_selected = self.find_element(by=by, expression=expression, target=target).is_selected()
        logger.info(f"获取元素是否选中成功: {is_selected}", extra={'identification': f"operationId:{self.operationId}"})
        return is_selected

    @exception_handler(message='获取元素是否启用失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_enabled(self, by, expression, target):
        """获取元素是否启用"""
        is_enabled = self.find_element(by=by, expression=expression, target=target).is_enabled()
        logger.info(f"获取元素是否启用成功:{is_enabled}", extra={'identification': f"operationId:{self.operationId}"})
        return is_enabled

    @exception_handler(message='获取元素是否显示失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_displayed(self, by, expression, target):
        """判断元素是否显示"""
        is_displayed = self.find_element(by=by, expression=expression, target=target).is_displayed()
        logger.info(f"获取元素是否显示:{is_displayed}", extra={'identification': f"operationId:{self.operationId}"})
        return is_displayed

    @exception_handler(message='获取元素是否存在失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def get_ele_existed(self, by, expression, target):
        """获取元素是否存在"""
        try:
            self.driver.find_element(self.get_locator(by), expression)
            logger.info(f"元素存在{target}：By: {by} Expression: {expression}", extra={'identification': f"operationId:{self.operationId}"})
            return True
        except NoSuchElementException:
            logger.info(f"元素不存在{target}：By: {by} Expression: {expression}", extra={'identification': f"operationId:{self.operationId}"})
            return False


if __name__ == '__main__':
    Operation().get_ele_attribute(locator='id', element='123', name='foo')
