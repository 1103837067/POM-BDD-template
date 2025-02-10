import allure
from pytest_bdd import given, when, then, parsers, scenario
from pages.baidu_page import BaiduPage

@allure.feature("百度搜索功能")
@scenario("../tests/features/baidu_search.feature", "在百度中搜索关键词")
def test_baidu_search():
    """百度搜索测试"""
    pass

@given("我打开百度首页", target_fixture="setup_page")
def open_baidu(page, baidu_page):
    baidu_page.navigate()
    return baidu_page

@when(parsers.parse('我在搜索框中输入"{keyword}"'))
def input_keyword(setup_page, keyword):
    setup_page.input_search_keyword(keyword)

@when("点击搜索按钮")
def click_search(setup_page):
    setup_page.click_search()

@then(parsers.parse('我应该看到包含"{expected_text}"的搜索结果'))
def verify_search_results(setup_page, expected_text):
    assert setup_page.verify_search_results(expected_text), \
        f"未能在搜索结果中找到预期文本: {expected_text}" 