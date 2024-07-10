import json

from Core.web.driver.browserOpt import Browser
from Core.web.driver.pageOpt import Page
from Core.web.driver.scenarioOpt import Scenario
from Core.web.driver.assertionOpt import Assertion
from Core.web.driver.relationOpt import Relation
from Core.web.driver.conditionOpt import Condition


class AllOpt(Browser, Page, Relation, Condition, Assertion, Scenario):
    def set(self, driver=None, params=None):
        if driver is not None:
            self.driver = driver

        if params is not None:
            self.params = params

    def clean(self, closeDriver=True):
        if closeDriver is True:
            self.driver.quit()
            self.driver = None
        self.params = None


operation_instance = AllOpt()

OPERATIONS_MAP = {
    'browser': {
        '最大化窗口': operation_instance.max_window,
        '最小化窗口': operation_instance.min_window,
        '全屏窗口': operation_instance.full_window,
        '设置窗口位置': operation_instance.set_position_window,
        '设置窗口大小': operation_instance.set_size_window,
        '切换窗口': operation_instance.switch_to_window,
        '关闭窗口': operation_instance.close_window,
        '屏幕截图': operation_instance.save_screenshot,
        '单击跳转新窗口': operation_instance.click_to_new_window,
        '打开网页': operation_instance.open_url,
        '刷新': operation_instance.refresh,
        '后退': operation_instance.back,
        '前进': operation_instance.forward,
        '强制等待': operation_instance.sleep,
        '隐式等待': operation_instance.implicitly_wait,
        '添加cookie': operation_instance.add_cookie,
        '删除cookie': operation_instance.delete_cookie,
        '删除cookies': operation_instance.delete_cookies,
        '执行脚本': operation_instance.execute_script,
        '执行异步脚本': operation_instance.execute_async_script,
    },
    'page': {
        '切换frame': operation_instance.switch_frame,
        '返回默认frame': operation_instance.switch_content,
        '输入': operation_instance.input_text,
        '单击': operation_instance.click,
        '返回父级frame': operation_instance.switch_parent,
        '弹出框确认': operation_instance.alert_accept,
        '弹出框输入': operation_instance.alert_input,
        '弹出框取消': operation_instance.alert_cancel,
        '鼠标单击': operation_instance.click_and_hold,
        '清空': operation_instance.clear,
        '提交': operation_instance.submit,
        '单击保持': operation_instance.click_and_hold,
        '等待元素出现': operation_instance.wait_element_appear,
        '等待元素消失': operation_instance.wait_element_disappear,
        '右键点击': operation_instance.context_click,
        '双击': operation_instance.double_click

    },
    'assertion': {
        '断言页面标题': operation_instance.assert_page_title,
        '断言页面url': operation_instance.assert_page_url,
        '断言页面源码': operation_instance.assert_page_source,
        '断言元素文本': operation_instance.assert_ele_text,
        "断言元素tag": operation_instance.assert_ele_tag,
        "断言元素尺寸": operation_instance.assert_ele_size,
        "断言元素高度": operation_instance.assert_ele_height,
        "断言元素宽度": operation_instance.assert_ele_width,
        "断言元素位置": operation_instance.assert_ele_location,
        "断言元素X坐标": operation_instance.assert_ele_x,
        "断言元素Y坐标": operation_instance.assert_ele_y,
        "断言元素属性": operation_instance.assert_ele_attribute,
        "断言元素是否选中": operation_instance.assert_ele_selected,
        "断言元素是否启用": operation_instance.assert_ele_enabled,
        "断言元素是否显示": operation_instance.assert_ele_displayed,
        "断言元素css样式": operation_instance.assert_ele_css,
        "断言元素是否存在": operation_instance.assert_ele_existed,
        "断言窗口位置": operation_instance.assert_window_position,
        "断言窗口X坐标": operation_instance.assert_window_x,
        "断言窗口Y坐标": operation_instance.assert_window_y,
        "断言窗口尺寸": operation_instance.assert_window_size,
        "断言窗口宽度": operation_instance.assert_window_width,
        "断言窗口高度": operation_instance.assert_window_height,
        "断言cookies": operation_instance.assert_cookies,
        "断言cookie": operation_instance.assert_cookie,
    },
    'relation': {
        "提取页面标题": operation_instance.save_page_title,
        "提取页面url": operation_instance.save_page_url,
        "提取元素源码": operation_instance.save_ele_html,
        "提取元素文本": operation_instance.save_ele_text,
        "提取元素tag": operation_instance.save_ele_tag,
        "提取元素尺寸": operation_instance.save_ele_size,
        "提取元素高度": operation_instance.save_ele_height,
        "提取元素宽度": operation_instance.save_ele_width,
        "提取元素位置": operation_instance.save_ele_location,
        "提取元素X坐标": operation_instance.save_ele_x,
        "提取元素Y坐标": operation_instance.save_ele_y,
        "提取元素属性": operation_instance.save_ele_attribute,
        "提取元素css样式": operation_instance.save_ele_css,
        "提取窗口位置": operation_instance.save_window_position,
        "提取窗口X坐标": operation_instance.save_window_x,
        "提取窗口Y坐标": operation_instance.save_window_y,
        "提取窗口尺寸": operation_instance.save_window_size,
        "提取窗口宽度": operation_instance.save_window_width,
        "提取窗口高度": operation_instance.save_window_height,
        "提取当前窗口句柄": operation_instance.save_current_handle,
        "提取所有窗口句柄": operation_instance.save_all_handle,
        "提取cookies": operation_instance.save_cookies,
        "提取cookie": operation_instance.save_cookie,
    },
    'condition': {
        "判断页面标题": operation_instance.condition_page_title,
        "判断页面url": operation_instance.condition_page_url,
        "判断页面源码": operation_instance.condition_page_source,
        "判断元素文本": operation_instance.condition_ele_text,
        "判断元素tag": operation_instance.condition_ele_tag,
        "判断元素尺寸": operation_instance.condition_ele_size,
        "判断元素高度": operation_instance.condition_ele_height,
        "判断元素宽度": operation_instance.condition_ele_width,
        "判断元素位置": operation_instance.condition_ele_location,
        "判断元素X坐标": operation_instance.condition_ele_x,
        "判断元素Y坐标": operation_instance.condition_ele_y,
        "判断元素属性": operation_instance.condition_ele_attribute,
        "判断元素是否选中": operation_instance.condition_ele_selected,
        "判断元素是否启用": operation_instance.condition_ele_enabled,
        "判断元素是否显示": operation_instance.condition_ele_displayed,
        "判断元素css样式": operation_instance.condition_ele_css,
        "判断元素是否存在": operation_instance.condition_ele_existed,
        "判断窗口位置": operation_instance.condition_window_position,
        "判断窗口X坐标": operation_instance.condition_window_x,
        "判断窗口Y坐标": operation_instance.condition_window_y,
        "判断窗口尺寸": operation_instance.condition_window_size,
        "判断窗口宽度": operation_instance.condition_window_width,
        "判断窗口高度": operation_instance.condition_window_height,
        "判断cookies": operation_instance.condition_cookies,
        "判断cookie": operation_instance.condition_cookie
    },
    'scenario': {
        '云平台项目列表': operation_instance.project_list,
        '云平台菜单点击': operation_instance.menu
    }
}