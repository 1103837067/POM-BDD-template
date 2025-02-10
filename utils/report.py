import os
import allure
from typing import Optional, Dict, Any
from datetime import datetime
from .logger import Logger
from .helpers import create_dir_if_not_exists, get_timestamp

class TestReport:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.screenshot_dir = "reports/screenshots"
        self.create_report_dirs()

    def create_report_dirs(self):
        """创建报告相关目录"""
        create_dir_if_not_exists(self.screenshot_dir)
        create_dir_if_not_exists("reports/allure-results")

    def attach_screenshot(self, page, name: Optional[str] = None) -> None:
        """
        添加截图到报告
        :param page: playwright页面对象
        :param name: 截图名称
        """
        try:
            screenshot_name = name or f"screenshot_{get_timestamp()}"
            screenshot_path = os.path.join(self.screenshot_dir, f"{screenshot_name}.png")
            
            # 保存截图
            page.screenshot(path=screenshot_path)
            
            # 添加到Allure报告
            allure.attach.file(
                screenshot_path,
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")

    def attach_html(self, content: str, name: str) -> None:
        """
        添加HTML内容到报告
        :param content: HTML内容
        :param name: 附件名称
        """
        try:
            allure.attach(
                content,
                name=name,
                attachment_type=allure.attachment_type.HTML
            )
        except Exception as e:
            self.logger.error(f"Failed to attach HTML content: {str(e)}")

    def attach_text(self, content: str, name: str) -> None:
        """
        添加文本内容到报告
        :param content: 文本内容
        :param name: 附件名称
        """
        try:
            allure.attach(
                content,
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            self.logger.error(f"Failed to attach text content: {str(e)}")

    def add_test_step(self, step_name: str, status: str = "passed") -> None:
        """
        添加测试步骤
        :param step_name: 步骤名称
        :param status: 步骤状态
        """
        with allure.step(step_name):
            if status == "failed":
                allure.attach(
                    "Step failed",
                    name="Status",
                    attachment_type=allure.attachment_type.TEXT
                )

    def add_test_description(self, description: str) -> None:
        """
        添加测试描述
        :param description: 描述内容
        """
        allure.dynamic.description(description)

    def add_test_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        添加测试参数
        :param parameters: 参数字典
        """
        for name, value in parameters.items():
            allure.dynamic.parameter(name, value) 