from Core.web.driver import Operation


class Condition(Operation):
    """条件类操作"""

    def condition_page_title(self, assertion, expect):
        """判断页面标题"""
        return self.compare_condition(assertion=assertion, actual=self.get_page_title(), expect=expect, title="判断页面标题")

    def condition_page_url(self, assertion, expect):
        """判断页面url"""
        return self.compare_condition(assertion=assertion, actual=self.get_page_url(), expect=expect, title="判断页面url")

    def condition_page_source(self, assertion, expect):
        """判断页面源码"""
        return self.compare_condition(assertion=assertion, actual=self.get_page_source(), expect=expect, title="判断页面源码")

    def condition_ele_text(self, by, expression, target, assertion, expect):
        """判断元素文本"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_text(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素文本")

    def condition_ele_tag(self, by, expression, target, assertion, expect):
        """判断元素tag"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_tag(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素tag")

    def condition_ele_size(self, by, expression, target, assertion, expect):
        """判断元素尺寸"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_size(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素尺寸")

    def condition_ele_height(self, by, expression, target, assertion, expect):
        """判断元素高度"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_height(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素高度")

    def condition_ele_width(self, by, expression, target, assertion, expect):
        """判断元素宽度"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_width(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素宽度")

    def condition_ele_location(self, by, expression, target, assertion, expect):
        """判断元素位置"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_location(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素位置")

    def condition_ele_x(self, by, expression, target, assertion, expect):
        """判断元素X坐标"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_x(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素X坐标")

    def condition_ele_y(self, by, expression, target, assertion, expect):
        """判断元素Y坐标"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_y(by=by, expression=expression, target=target),
                                      expect=expect,
                                      title="判断元素Y坐标")

    def condition_ele_attribute(self, by, expression, target, name, assertion, expect):
        """判断元素属性"""
        return self.compare_condition(assertion=assertion,
                                      actual=self.get_ele_attribute(by=by, expression=expression, target=target, name=name), expect=expect,
                                      title="判断元素属性")

    def condition_ele_selected(self, by, expression, target):
        """判断元素是否选中"""
        return self.compare_condition(assertion='isTrue', actual=self.get_ele_selected(by=by, expression=expression, target=target),
                                      title="判断元素是否选中")

    def condition_ele_enabled(self, by, expression, target):
        """判断元素是否启用"""
        return self.compare_condition(assertion='isTrue', actual=self.get_ele_enabled(by=by, expression=expression, target=target),
                                      title="判断元素是否启用")

    def condition_ele_displayed(self, by, expression, target):
        """判断元素是否显示"""
        return self.compare_condition(assertion='isTrue', actual=self.get_ele_displayed(by=by, expression=expression, target=target),
                                      title="判断元素是否显示")

    def condition_ele_css(self, by, expression, target, name, assertion, expect):
        """判断元素css样式"""
        return self.compare_condition(assertion=assertion, actual=self.get_ele_css(by=by, expression=expression, target=target, name=name),
                                      expect=expect,
                                      title="判断元素css样式")

    def condition_ele_existed(self, by, expression, target):
        """判断元素是否存在"""
        return self.compare_condition(assertion='isTrue', actual=self.get_ele_css(by=by, expression=expression, target=target),
                                      title="判断元素是否存在")

    def condition_window_position(self, assertion, expect):
        """判断窗口位置"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_position(), expect=expect, title="判断窗口位置")

    def condition_window_x(self, assertion, expect):
        """判断窗口X坐标"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_x(), expect=expect, title="判断窗口X坐标")

    def condition_window_y(self, assertion, expect):
        """判断窗口Y坐标"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_y(), expect=expect, title="判断窗口Y坐标")

    def condition_window_size(self, assertion, expect):
        """判断窗口大小"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_size(), expect=expect, title="判断窗口大小")

    def condition_window_width(self, assertion, expect):
        """判断窗口宽度"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_width(), expect=expect, title="判断窗口宽度")

    def condition_window_height(self, assertion, expect):
        """判断窗口高度"""
        return self.compare_condition(assertion=assertion, actual=self.get_window_height(), expect=expect, title="判断窗口高度")

    def condition_cookies(self, assertion, expect):
        """判断cookies"""
        return self.compare_condition(assertion=assertion, actual=self.get_cookies(), expect=expect, title="判断cookies")

    def condition_cookie(self, name, assertion, expect):
        """判断cookie"""
        return self.compare_condition(assertion=assertion, actual=self.get_cookie(name=name), expect=expect, title=f"判断cookie: {name}")
