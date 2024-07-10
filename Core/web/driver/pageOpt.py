import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait, expected_conditions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Common.utils import exception_handler
from Common.logger import logger
from Core.web.driver import Operation, add_error_log


class Page(Operation):
    """网页类操作"""

    @exception_handler(message='切换frame失败: {target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def switch_frame(self, by, expression, target):
        """切换框架"""
        self.driver.switch_to.frame(self.find_element(by=by, expression=expression, target=target))
        logger.info(f"切换frame成功: {target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='返回默认框架失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def switch_content(self):
        """返回默认框架"""
        self.driver.switch_to.default_content()
        logger.info("返回默认框架成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='返回父框架失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def switch_parent(self):
        """返回父框架"""
        self.driver.switch_to.parent_frame()
        logger.info("返回父框架成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='执行弹出框确认失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def alert_accept(self):
        """弹出框确认"""
        alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
        alert.accept()
        logger.info("成功执行：弹出框确认", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='弹出框输入失败: {text}', throw_exception=RuntimeError, standby_func=add_error_log)
    def alert_input(self, text):
        """弹出框输入"""
        alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
        alert.send_keys(text)
        logger.info(f"弹出框输入成功: {text}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='弹出框取消失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def alert_cancel(self):
        """弹出框取消"""
        alert = wait.WebDriverWait(self.driver, timeout=30).until(expected_conditions.alert_is_present())
        alert.dismiss()
        logger.info("弹出框取消成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='鼠标单击失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def free_click(self):
        """鼠标单击"""
        ActionChains(self.driver).click().perform()
        logger.info("鼠标单击成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='清空失败 Target:{target}, Text: {text}', throw_exception=RuntimeError, standby_func=add_error_log)
    def clear(self, by, expression, target):
        """清空"""
        self.find_element(by=by, expression=expression, target=target).clear()
        logger.info(f"清空成功 Target:{target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='输入失败 Target:{target}, Text: {text}', throw_exception=RuntimeError, standby_func=add_error_log)
    def input_text(self, by, expression, target, text):
        """输入"""
        self.find_element(by=by, expression=expression, target=target).send_keys(text)
        logger.info(f"输入成功 Target:{target}, Text: {text}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='点击失败: {target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def click(self, by, expression, target):
        """单击"""
        self.find_element(by=by, expression=expression, target=target).click()
        logger.info(f"点击成功: {target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='提交失败: Target:{target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def submit(self, by, expression, target):
        """提交"""
        self.find_element(by=by, expression=expression, target=target).submit()
        logger.info(f"提交成功 Target:{target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='单击保持失败 Target:{target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def click_and_hold(self, by, expression, target):
        """单击保持"""
        ele = self.find_element(by=by, expression=expression, target=target)
        ActionChains(self.driver).click_and_hold(ele).perform()
        logger.info(f"单击保持成功 Target:{target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='右键点击执行失败 Target:{target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def context_click(self, by, expression, target):
        """右键点击"""
        ele = self.find_element(by=by, expression=expression, target=target)
        ActionChains(self.driver).context_click(ele).perform()
        logger.info("右键点击成功执行 Target:{target}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='双击执行失败 Target:{target}', throw_exception=RuntimeError, standby_func=add_error_log)
    def double_click(self, by, expression, target):
        """双击"""
        ele = self.find_element(by=by, expression=expression, target=target)
        ActionChains(self.driver).double_click(ele).perform()
        logger.info("双击成功执行 Target:{target}", extra={'identification': f"operationId:{self.operationId}"})

    def drag_and_drop(self, start_element, end_element):
        """拖拽"""
        try:
            ele = self.find_element(start_element)
            tar_ele = self.find_element(end_element)
            ActionChains(self.driver).drag_and_drop(ele, tar_ele).perform()
            self.test.debugLog("成功执行drag and drop to element")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行drag and drop to element")
            raise e

    def drag_and_drop_by_offset(self, element, x, y):
        """偏移拖拽"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).drag_and_drop_by_offset(ele, x, y).perform()
            self.test.debugLog("成功执行drag and drop to (%s, %s)" % (x, y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行drag and drop to (%s, %s)" % (x, y))
            raise e

    def key_down(self, element, value):
        """按下键位"""
        try:
            ele = self.find_element(element)
            if hasattr(Keys, value.upper()):
                keys = getattr(Keys, value)
            else:
                raise Exception("键位%s不存在" % value)
            ActionChains(self.driver).key_down(keys, ele).perform()
            self.test.debugLog("成功执行key down %s" % value)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行key down %s" % value)
            raise e

    def key_up(self, element, value):
        """释放键位"""
        try:
            ele = self.find_element(element)
            if hasattr(Keys, value.upper()):
                keys = getattr(Keys, value)
            else:
                raise Exception("键位%s不存在" % value)
            ActionChains(self.driver).key_up(keys, ele).perform()
            self.test.debugLog("成功执行key up %s" % value)
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行key up %s" % value)
            raise e

    def move_by_offset(self, x, y):
        """鼠标移动到坐标"""
        try:
            ActionChains(self.driver).move_by_offset(x, y).perform()
            self.test.debugLog("成功执行move mouse to (%s, %s)" % (x, y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to (%s, %s)" % (x, y))
            raise e

    def move_to_element(self, element):
        """鼠标移动到元素"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.test.debugLog("成功执行move mouse to element")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to element")
            raise e

    def move_to_element_with_offset(self, element, x, y):
        """鼠标移动到元素坐标"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).move_to_element_with_offset(ele, x, y).perform()
            self.test.debugLog("成功执行move mouse to element with (%s, %s)" % (x, y))
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行move mouse to element with (%s, %s)" % (x, y))
            raise e

    def release(self, element):
        """释放点击保持状态"""
        try:
            ele = self.find_element(element)
            ActionChains(self.driver).release(ele).perform()
            self.test.debugLog("成功执行release mouse")
        except NoSuchElementException as e:
            raise e
        except Exception as e:
            self.test.errorLog("无法执行release mouse")
            raise e

    @exception_handler(message='"等待元素出现执行失败 Target: {target},Second:{second} "', throw_exception=RuntimeError, standby_func=add_error_log)
    def wait_element_appear(self, by, expression, target, second):
        """等待元素出现"""

        WebDriverWait(self.driver, second, 0.2).until(
            expected_conditions.presence_of_element_located((self.get_locator(by), expression))
        )
        logger.info(f"等待元素出现执行成功 Target: {target},Second:{second}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='"等待元素消失执行失败 Target: {target},Second:{second} "', throw_exception=RuntimeError, standby_func=add_error_log)
    def wait_element_disappear(self, by, expression, target, second):
        """等待元素消失"""
        WebDriverWait(self.driver, second, 0.2).until_not(
            expected_conditions.presence_of_element_located((self.get_locator(by), expression))
        )
        logger.info(f"等待元素消失执行成功 Target: {target},Second:{second}", extra={'identification': f"operationId:{self.operationId}"})
