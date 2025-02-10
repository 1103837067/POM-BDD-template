from playwright.sync_api import Page, expect
import allure
import time
from typing import Optional, Any, List, Callable
import logging
from functools import wraps

class PageException(Exception):
    """基础页面异常类"""
    pass

class ElementNotVisibleException(PageException):
    """元素不可见异常"""
    pass

class ElementNotPresentException(PageException):
    """元素不存在异常"""
    pass

class ElementActionException(PageException):
    """元素操作异常"""
    pass

def retry(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"WARNING: {func.__name__} 第 {attempt + 1} 次尝试失败: {str(e)}")
                    if attempt < retries - 1:
                        time.sleep(delay)
                    continue
            print(f"ERROR: {func.__name__} 在 {retries} 次尝试后仍然失败")
            raise last_exception
        return wrapper
    return decorator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000  # 默认超时时间10秒

    @allure.step("等待元素可见")
    def wait_for_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"元素 {selector} 在 {timeout or self.timeout}ms 内未变为可见"
            raise ElementNotVisibleException(error_msg) from e

    @allure.step("等待元素存在")
    def wait_for_present(self, selector: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_selector(selector, state="attached", timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"元素 {selector} 在 {timeout or self.timeout}ms 内未出现在DOM中"
            raise ElementNotPresentException(error_msg) from e

    @retry(retries=3)
    @allure.step("点击元素")
    def click(self, selector: str, force: bool = False) -> None:
        try:
            self.wait_for_visible(selector)
            self.page.click(selector, force=force)
        except ElementNotVisibleException:
            raise
        except Exception as e:
            error_msg = f"点击元素 {selector} 失败"
            raise ElementActionException(error_msg) from e

    @retry(retries=3)
    @allure.step("输入文本")
    def fill(self, selector: str, text: str) -> None:
        try:
            self.wait_for_visible(selector)
            self.page.fill(selector, text)
        except Exception as e:
            error_msg = f"在元素 {selector} 中输入文本失败"
            raise ElementActionException(error_msg) from e

    @allure.step("获取元素文本")
    def get_text(self, selector: str) -> str:
        self.wait_for_visible(selector)
        return self.page.text_content(selector)

    @allure.step("获取元素的属性值")
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        self.wait_for_present(selector)
        element = self.page.locator(selector)
        return element.get_attribute(attribute)

    @allure.step("检查元素是否可见")
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        try:
            self.wait_for_visible(selector, timeout=timeout or 1000)
            return True
        except:
            return False

    @allure.step("获取元素列表")
    def get_elements(self, selector: str) -> List[Any]:
        return self.page.locator(selector).all()

    @allure.step("等待加载状态")
    def wait_for_loading(self, timeout: Optional[int] = None) -> None:
        self.page.wait_for_load_state("load", timeout=timeout or self.timeout)
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout or self.timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout or self.timeout)

    @allure.step("滚动到元素")
    def scroll_into_view(self, selector: str) -> None:
        self.page.locator(selector).scroll_into_view_if_needed()

    @allure.step("悬停在元素上")
    def hover(self, selector: str) -> None:
        self.wait_for_visible(selector)
        self.page.hover(selector)

    @allure.step("按键输入")
    def press_key(self, selector: str, key: str) -> None:
        self.wait_for_visible(selector)
        self.page.press(selector, key)

    @allure.step("清除输入框")
    def clear_input(self, selector: str) -> None:
        self.wait_for_visible(selector)
        self.page.fill(selector, "")

    @allure.step("双击元素")
    def double_click(self, selector: str) -> None:
        self.wait_for_visible(selector)
        self.page.dblclick(selector)

    @allure.step("获取页面标题")
    def get_title(self) -> str:
        return self.page.title()

    @allure.step("获取当前URL")
    def get_url(self) -> str:
        return self.page.url

    @allure.step("刷新页面")
    def refresh(self) -> None:
        self.page.reload()

    @allure.step("后退")
    def go_back(self) -> None:
        self.page.go_back()

    @allure.step("前进")
    def go_forward(self) -> None:
        self.page.go_forward()

    @allure.step("截图")
    def take_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("等待时间")
    def wait(self, milliseconds: int) -> None:
        time.sleep(milliseconds / 1000)

    @allure.step("执行JavaScript")
    def evaluate(self, expression: str, arg: Optional[Any] = None) -> Any:
        return self.page.evaluate(expression, arg)

    @allure.step("断言元素可见")
    def assert_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout or self.timeout)

    @allure.step("断言元素包含文本")
    def assert_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout or self.timeout)

    @allure.step("断言元素属性")
    def assert_attribute(self, selector: str, attribute: str, value: str, timeout: Optional[int] = None) -> None:
        expect(self.page.locator(selector)).to_have_attribute(attribute, value, timeout=timeout or self.timeout)

    @allure.step("等待元素消失")
    def wait_for_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"元素 {selector} 在 {timeout or self.timeout}ms 内未消失"
            raise ElementActionException(error_msg) from e

    @allure.step("等待URL包含指定文本")
    def wait_for_url(self, url_text: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_url(f"**/*{url_text}*", timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"URL在 {timeout or self.timeout}ms 内未包含文本: {url_text}"
            raise ElementActionException(error_msg) from e

    @allure.step("选择下拉框选项")
    def select_option(self, selector: str, value: str) -> None:
        try:
            self.wait_for_visible(selector)
            self.page.select_option(selector, value=value)
        except Exception as e:
            error_msg = f"在下拉框 {selector} 中选择选项 {value} 失败"
            raise ElementActionException(error_msg) from e

    @allure.step("获取元素数量")
    def get_count(self, selector: str) -> int:
        return len(self.page.locator(selector).all())

    @allure.step("等待元素数量达到预期")
    def wait_for_count(self, selector: str, count: int, timeout: Optional[int] = None) -> None:
        try:
            self.page.locator(selector).nth(count - 1).wait_for(timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"元素 {selector} 数量在 {timeout or self.timeout}ms 内未达到 {count}"
            raise ElementActionException(error_msg) from e

    @allure.step("获取元素的CSS属性值")
    def get_css_property(self, selector: str, property_name: str) -> str:
        element = self.page.locator(selector)
        return element.evaluate(f"element => window.getComputedStyle(element).{property_name}")

    @allure.step("检查元素是否启用")
    def is_enabled(self, selector: str) -> bool:
        return self.page.locator(selector).is_enabled()

    @allure.step("检查元素是否被选中")
    def is_checked(self, selector: str) -> bool:
        return self.page.locator(selector).is_checked()

    @allure.step("拖拽元素")
    def drag_and_drop(self, source: str, target: str) -> None:
        try:
            self.page.drag_and_drop(source, target)
        except Exception as e:
            error_msg = f"拖拽元素从 {source} 到 {target} 失败"
            raise ElementActionException(error_msg) from e

    @allure.step("上传文件")
    def upload_file(self, selector: str, file_path: str) -> None:
        try:
            self.page.set_input_files(selector, file_path)
        except Exception as e:
            error_msg = f"上传文件到 {selector} 失败"
            raise ElementActionException(error_msg) from e

    @allure.step("切换到iframe")
    def switch_to_frame(self, frame_selector: str) -> None:
        try:
            frame = self.page.frame_locator(frame_selector)
            if not frame:
                raise ElementNotPresentException(f"未找到iframe: {frame_selector}")
        except Exception as e:
            error_msg = f"切换到iframe {frame_selector} 失败"
            raise ElementActionException(error_msg) from e

    @allure.step("等待网络请求完成")
    def wait_for_request(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_request(url_pattern, timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"等待请求 {url_pattern} 超时"
            raise ElementActionException(error_msg) from e

    @allure.step("等待网络响应完成")
    def wait_for_response(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        try:
            self.page.wait_for_response(url_pattern, timeout=timeout or self.timeout)
        except Exception as e:
            error_msg = f"等待响应 {url_pattern} 超时"
            raise ElementActionException(error_msg) from e 