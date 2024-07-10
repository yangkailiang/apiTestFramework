import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from Common.utils import exception_handler
from Common.logger import logger
from Core.web.driver import Operation, add_error_log


class Scenario(Operation):
    """场景类类操作"""

    @exception_handler(message='云平台项目列表选中项目报错: ProjectName:{projectName}', throw_exception=RuntimeError,
                       standby_func=add_error_log)
    def project_list(self, projectName):
        """ 云平台项目列表组件 """
        elements = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.project-list-item')))
        logger.info("获取项目列表成功", extra={'identification': f"operationId:{self.operationId}"})
        for element in elements:
            name = element.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div').text
            logger.info(f"循环获取项目名称：{name}", extra={'identification': f"operationId:{self.operationId}"})
            if projectName in name:
                element.find_element(By.CSS_SELECTOR, 'div > .enter-button').click()
                logger.info(f"进入项目成功：{name}", extra={'identification': f"operationId:{self.operationId}"})

                return
        raise RuntimeError(f"未能选中项目：{projectName}")

    @exception_handler(message='菜单组件选中失败 FirstLevelMenu:{firstLevelMenu} SecondLevelMenu:{secondLevelMenu}',
                       throw_exception=RuntimeError, standby_func=add_error_log)
    def menu(self, firstLevelMenu, secondLevelMenu=None):
        firstLevelMenuElements = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '[role="menuitem"]'))
        )
        for firstLevelMenuElement in firstLevelMenuElements:
            try:
                firstLevelMenuText = firstLevelMenuElement.find_element(By.CSS_SELECTOR, 'span:nth-child(2)').text
            except:
                continue
            logger.info(f"当前获取到一级菜单: {firstLevelMenuText}", extra={'identification': f"operationId:{self.operationId}"})
            if firstLevelMenu == firstLevelMenuText:
                firstLevelMenuElement.click()
                logger.info(f"点击一级菜单成功: {firstLevelMenuText}", extra={'identification': f"operationId:{self.operationId}"})
                if secondLevelMenu:
                    secondMenuElements = WebDriverWait(firstLevelMenuElement, 10).until(
                        expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.ant-menu-item'))
                    )
                    time.sleep(1)
                    for secondLevelMenuElement in secondMenuElements:
                        secondLevelMenuText = secondLevelMenuElement.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
                        logger.info(f"当前二级菜单：{secondLevelMenuText}, 预期选中菜单：{secondLevelMenu}", extra={'identification': f"operationId:{self.operationId}"})
                        if secondLevelMenuText == secondLevelMenu:
                            secondLevelMenuElement.click()
                            logger.info(f"点击二级菜单成功：{secondLevelMenuText}")
                            return
                        raise RuntimeError(f"菜单组件选中失败: FirstLevelMenu:{firstLevelMenu} SecondLevelMenu:{secondLevelMenu}")
                return

        raise RuntimeError(f"菜单组件选中失败: FirstLevelMenu:{firstLevelMenu} SecondLevelMenu:{secondLevelMenu}")
