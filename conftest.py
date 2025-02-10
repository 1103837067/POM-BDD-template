import pytest
from playwright.sync_api import sync_playwright
import allure
from config.config import TestConfig
from pages.baidu_page import BaiduPage

# ============================
# 基础 Fixtures
# ============================

@pytest.fixture(scope="session")
def test_config():
    """全局测试配置"""
    return TestConfig()

@pytest.fixture(scope="session")
def playwright():
    """Playwright 实例"""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright, test_config):
    """浏览器实例"""
    browser = getattr(playwright, test_config.browser_type).launch(**test_config.get_browser_launch_options())
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser, test_config):
    """浏览器上下文"""
    context = browser.new_context(**test_config.get_context_options())
    context.set_default_timeout(test_config.timeout)
    context.set_default_navigation_timeout(test_config.navigation_timeout)
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """页面实例"""
    page = context.new_page()
    yield page
    page.close()

# ============================
# 页面对象 Fixtures
# ============================

@pytest.fixture
def baidu_page(page):
    """百度页面对象"""
    return BaiduPage(page)

# ============================
# 错误处理和报告
# ============================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时截图"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs["page"]
            allure.attach(
                page.screenshot(),
                name='failure_screenshot',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to capture failure evidence: {e}") 