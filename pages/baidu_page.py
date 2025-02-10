from .base_page import BasePage
import allure

class BaiduPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # 页面元素定位器
        self._search_input = "#kw"
        self._search_button = "#su"
        self._search_results = ".result-op"

    @allure.step("打开百度首页")
    def navigate(self):
        self.page.goto("https://www.baidu.com")
        self.wait_for_loading()

    @allure.step("输入搜索关键词: {keyword}")
    def input_search_keyword(self, keyword: str):
        self.fill(self._search_input, keyword)

    @allure.step("点击搜索按钮")
    def click_search(self):
        self.click(self._search_button)
        self.wait_for_loading()

    @allure.step("检查搜索结果是否包含: {expected_text}")
    def verify_search_results(self, expected_text: str) -> bool:
        self.wait_for_visible(self._search_results, timeout=10000)
        page_content = self.page.content()
        return expected_text in page_content

    @allure.step("获取搜索结果列表")
    def get_search_results(self) -> list:
        return self.get_elements(self._search_results)

    @allure.step("获取搜索框的值")
    def get_search_input_value(self) -> str:
        return self.get_attribute(self._search_input, "value")

    @allure.step("清空搜索框")
    def clear_search_input(self):
        self.clear_input(self._search_input) 