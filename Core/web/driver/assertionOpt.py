import sys

from selenium.common.exceptions import NoSuchElementException

from Core.web.driver import Operation


class Assertion(Operation):
    """断言类操作"""

    def assert_page_title(self, assertion, expect, **kwargs):
        """判断页面标题"""
        return self.compare(assertion=assertion, actual=self.get_page_title(), expect=expect, title="判断页面标题", **kwargs)

    def assert_page_url(self, assertion, expect, **kwargs):
        """判断页面url"""
        return self.compare(assertion=assertion, actual=self.get_page_url(), expect=expect, title="判断页面url", **kwargs)

    def assert_page_source(self, assertion, expect, **kwargs):
        """判断页面源码"""
        return self.compare(assertion=assertion, actual=self.get_page_source(), expect=expect, title="判断页面源码", **kwargs)

    def assert_ele_text(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素文本"""
        return self.compare(assertion=assertion, actual=self.get_ele_text(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素文本", **kwargs)

    def assert_ele_tag(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素tag"""
        return self.compare(assertion=assertion, actual=self.get_ele_tag(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素tag", **kwargs)

    def assert_ele_size(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素尺寸"""
        return self.compare(assertion=assertion, actual=self.get_ele_size(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素尺寸", **kwargs)

    def assert_ele_height(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素高度"""
        return self.compare(assertion=assertion, actual=self.get_ele_height(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素高度", **kwargs)

    def assert_ele_width(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素宽度"""
        return self.compare(assertion=assertion, actual=self.get_ele_width(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素宽度", **kwargs)

    def assert_ele_location(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素位置"""
        return self.compare(assertion=assertion, actual=self.get_ele_location(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素位置", **kwargs)

    def assert_ele_x(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素X坐标"""
        return self.compare(assertion=assertion, actual=self.get_ele_x(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素X坐标", **kwargs)

    def assert_ele_y(self, by, expression, target, assertion, expect, **kwargs):
        """判断元素Y坐标"""
        return self.compare(assertion=assertion, actual=self.get_ele_y(by=by, expression=expression, target=target), expect=expect,
                            title="判断元素Y坐标", **kwargs)

    def assert_ele_attribute(self, by, expression, target, name, assertion, expect, **kwargs):
        """判断元素属性"""
        return self.compare(assertion=assertion, actual=self.get_ele_attribute(by=by, expression=expression, target=target, name=name), expect=expect,
                            title="判断元素属性", **kwargs)

    def assert_ele_selected(self, by, expression, target, **kwargs):
        """判断元素是否选中"""
        return self.compare(assertion='isTrue', actual=self.get_ele_selected(by=by, expression=expression, target=target), title="判断元素是否选中", **kwargs)

    def assert_ele_enabled(self, by, expression, target, **kwargs):
        """判断元素是否启用"""
        return self.compare(assertion='isTrue', actual=self.get_ele_enabled(by=by, expression=expression, target=target), title="判断元素是否启用", **kwargs)

    def assert_ele_displayed(self, by, expression, target, **kwargs):
        """判断元素是否显示"""
        return self.compare(assertion='isTrue', actual=self.get_ele_displayed(by=by, expression=expression, target=target), title="判断元素是否显示", **kwargs)

    def assert_ele_css(self, by, expression, target, name, assertion, expect, **kwargs):
        """判断元素css样式"""
        return self.compare(assertion=assertion, actual=self.get_ele_css(by=by, expression=expression, target=target, name=name), expect=expect,
                            title="判断元素css样式", **kwargs)

    def assert_ele_existed(self, by, expression, target, **kwargs):
        """判断元素是否存在"""
        return self.compare(assertion='isTrue', actual=self.get_ele_css(by=by, expression=expression, target=target),
                            title="判断元素是否存在", **kwargs)

    def assert_window_position(self, assertion, expect, **kwargs):
        """判断窗口位置"""
        return self.compare(assertion=assertion, actual=self.get_window_position(), expect=expect, title="判断窗口位置", **kwargs)

    def assert_window_x(self, assertion, expect, **kwargs):
        """判断窗口X坐标"""
        return self.compare(assertion=assertion, actual=self.get_window_x(), expect=expect, title="判断窗口X坐标", **kwargs)

    def assert_window_y(self, assertion, expect, **kwargs):
        """判断窗口Y坐标"""
        return self.compare(assertion=assertion, actual=self.get_window_y(), expect=expect, title="判断窗口Y坐标", **kwargs)

    def assert_window_size(self, assertion, expect, **kwargs):
        """判断窗口大小"""
        return self.compare(assertion=assertion, actual=self.get_window_size(), expect=expect, title="判断窗口大小", **kwargs)

    def assert_window_width(self, assertion, expect, **kwargs):
        """判断窗口宽度"""
        return self.compare(assertion=assertion, actual=self.get_window_width(), expect=expect, title="判断窗口宽度", **kwargs)

    def assert_window_height(self, assertion, expect, **kwargs):
        """判断窗口高度"""
        return self.compare(assertion=assertion, actual=self.get_window_height(), expect=expect, title="判断窗口高度", **kwargs)

    def assert_cookies(self, assertion, expect, **kwargs):
        """判断cookies"""
        return self.compare(assertion=assertion, actual=self.get_cookies(), expect=expect, title="判断cookies", **kwargs)

    def assert_cookie(self, name, assertion, expect, **kwargs):
        """判断cookie"""
        return self.compare(assertion=assertion, actual=self.get_cookie(name=name), expect=expect, title=f"判断cookie: {name}", **kwargs)
