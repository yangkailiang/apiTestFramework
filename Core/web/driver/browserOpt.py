import os

from datetime import datetime
from time import sleep
from uuid import uuid4

from Common.utils import exception_handler
from Common.logger import logger
from Core.web.driver import Operation, add_error_log
from Core.utils import url_join
from configs import IMAGE_PATH


class Browser(Operation):
    """浏览器类操作"""

    @exception_handler(message='窗口最大化失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def max_window(self):
        """最大化窗口"""
        self.driver.maximize_window()
        logger.info("窗口最大化成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='窗口最小化失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def min_window(self):
        """最小化窗口"""
        self.driver.minimize_window()
        logger.info("窗口最小化成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='全屏窗口失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def full_window(self):
        """全屏窗口"""
        self.driver.fullscreen_window()
        logger.info("全屏窗口成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='设置窗口位置失败: X: {x} - Y: {y}', throw_exception=RuntimeError, standby_func=add_error_log)
    def set_position_window(self, x, y):
        """设置窗口位置 0,0是左上角"""
        self.driver.set_window_position(x, y)
        logger.info(f"设置窗口位置成功: X: {x} - Y: {y}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='设置窗口大小失败: width: {width} - height: {height}', throw_exception=RuntimeError,
                       standby_func=add_error_log)
    def set_size_window(self, width, height):
        """设置窗口大小"""
        self.driver.set_window_size(width, height)
        logger.info(f"设置窗口大小成功: width: {width} - height: {height}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='切换窗口失败: index: {index} - title: {title}', throw_exception=RuntimeError, standby_func=add_error_log)
    def switch_to_window(self, index=None, title=None):
        """切换窗口"""
        # 获取当前页面所有的句柄
        window_handles = self.driver.window_handles
        if index is not None:
            self.driver.switch_to.window(window_handles[int(index)])
            logger.info("切换窗口成功: index: {index}", extra={'identification': f"operationId:{self.operationId}"})
            return
        if title is not None:
            current_window_handle = self.driver.current_window_handle
            for handle in window_handles:
                if handle == current_window_handle:
                    continue
                self.driver.switch_to.window(handle)
                if self.driver.title == title:
                    logger.info(f"切换窗口成功: title: {title}", extra={'identification': f"operationId:{self.operationId}"})
                    return

    @exception_handler(message='关闭窗口失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def close_window(self):
        """关闭窗口"""
        self.driver.close()
        logger.info("关闭窗口成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='屏幕截图失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def save_screenshot(self, result, **kwargs):
        """屏幕截图"""
        uid = f'{datetime.today().strftime("%Y%m%d")}_{str(uuid4())}'
        file_path = os.path.join(IMAGE_PATH, f"{uid}.png")
        with open(file_path, 'wb') as file:
            file.write(self.driver.get_screenshot_as_png())
        result.screenShotList.append(uid)
        logger.info("屏幕截图成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='单击跳转新窗口失败 By: {locator} Expression: {element}', throw_exception=RuntimeError,
                       standby_func=add_error_log)
    def click_to_new_window(self, locator, element):
        """单击跳转新窗口"""
        current = self.driver.window_handles
        # 点击打开新窗口
        self.find_element(locator=locator, element=element).click()
        # 等待新窗口出现
        current_time = datetime.now()
        while (datetime.now() - current_time).seconds < 60:
            if len(self.driver.window_handles) > len(current):
                for window_handle in self.driver.window_handles:
                    if window_handle not in current:
                        self.driver.switch_to.window(window_handle)
                        logger.info("单击跳转新窗口成功", extra={'identification': f"operationId:{self.operationId}"})
                        return
            sleep(2)

    @exception_handler(message='打开网页失败: {domain} {path}', throw_exception=RuntimeError, standby_func=add_error_log)
    def open_url(self, domain, path):
        """打开网页"""
        url = url_join(domain=domain, path=path)
        self.driver.get(url)
        logger.info(f"打开网页成功: {url}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='刷新页面失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def refresh(self):
        """刷新页面"""
        self.driver.refresh()
        logger.info(f"刷新页面成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='页面后退失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def back(self):
        """页面后退"""
        self.driver.back()
        logger.info(f"页面后退成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='页面前进失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def forward(self):
        """页面前进"""
        self.driver.forward()
        logger.info(f"页面前进成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='添加cookie失败: Name: {name}, Value:{value}', throw_exception=RuntimeError, standby_func=add_error_log)
    def add_cookie(self, name, value):
        """添加cookie"""
        self.driver.add_cookie({'name': name, 'value': value})
        logger.info(f"添加cookie成功: Name: {name}, Value:{value}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='删除cookie失败: Name: {name}', throw_exception=RuntimeError, standby_func=add_error_log)
    def delete_cookie(self, name):
        """删除cookie"""
        self.driver.delete_cookie(name)
        logger.info(f"删除cookie成功: Name: {name}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='删除所有cookie失败', throw_exception=RuntimeError, standby_func=add_error_log)
    def delete_cookies(self):
        """删除cookies"""
        self.driver.delete_all_cookies()
        logger.info("删除所有cookie成功", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='执行脚本失败: Script:{script}, Arg: {arg}', throw_exception=RuntimeError, standby_func=add_error_log)
    def execute_script(self, script, arg: tuple):
        """执行脚本"""
        self.driver.execute_script(script, *arg)
        logger.info(f"执行脚本成功: Script:{script}, Arg: {arg}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='执行异步脚本: Script:{script}, Arg: {arg}', throw_exception=RuntimeError, standby_func=add_error_log)
    def execute_async_script(self, script, arg: tuple):
        """执行异步脚本"""
        self.driver.execute_async_script(script, *arg)
        logger.info(f"执行异步脚本: Script:{script}, Arg: {arg}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='强制等待失败: Second: {second}', throw_exception=RuntimeError, standby_func=add_error_log)
    def sleep(self, second):
        """强制等待"""
        sleep(int(self))
        logger.info(f"强制等待成功: Second: {second}", extra={'identification': f"operationId:{self.operationId}"})

    @exception_handler(message='隐式等待设置失败: Second: {seconds}', throw_exception=RuntimeError, standby_func=add_error_log)
    def implicitly_wait(self, seconds):
        """隐式等待"""
        self.driver.implicitly_wait(seconds)
        logger.info(f'隐式等待设置成功: Second: {seconds}', extra={'identification': f"operationId:{self.operationId}"})