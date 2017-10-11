from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import time

class DriverWrapper:
    html_tags = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main", "map", "mark", "menu", "menuitem", "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]
    def get_element(self, selector, father = None):
        father = self.driver if father == None else father
        if selector == "":
            return father
        elif (selector[0] == '.' and './/' not in selector)\
            or selector[0] == '#' or selector in DriverWrapper.html_tags:
            return father.find_element_by_css_selector(selector)
        else:
            return father.find_element_by_xpath(selector)
    def get_elements(self, selector, father = None):
        father = self.driver if father == None else father
        if selector == "":
            return [father]
        elif (selector[0] == '.' and './/' not in selector)\
            or selector[0] == '#' or selector in DriverWrapper.html_tags:
            return father.find_elements_by_css_selector(selector)
        else:
            return father.find_elements_by_xpath(selector)



class MealPal(DriverWrapper):
    SELECTORS = {
        "login": "//input[@ng-model='formUser.email']",
        "password": "//input[@ng-model='formUser.password']",
        "search": "//input[@ng-model='vm.searchText']",
        "search_btn": ".search-button",
        "item": ".meal-box",
        "time_li": ".pickupTimes-list li",
        "reserve": ".mp-reserve-button"
    }
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password
        self.driver.set_window_size(1200,1000)
        self.wait_time = 2
    def get_elem(self, key, father = None):
        try:
            selector = MealPal.SELECTORS[key]
            return self.get_element(selector, father)
        except NoSuchElementException:
            print "{} not found".format(key)
            return None
    def login(self):
        self.driver.get("https://secure.mealpal.com/lunch")
        time.sleep(self.wait_time)
        login_input = self.get_elem("login")
        login_input.send_keys(self.username)
        pass_input = self.get_elem("password")
        pass_input.send_keys(self.password)
        pass_input.submit()
        time.sleep(self.wait_time)
    def search(self, search):
        search_input = self.get_elem("search")
        search_input.send_keys(search)
        time.sleep(self.wait_time)
        search_btn = self.get_elem("search_btn")
        search_btn.click()
    def select_first(self):
        time.sleep(self.wait_time)
        self.driver.execute_script("""
            $(".fade-box").css("display", "-webkit-box")
            $(".pickupTimes-list").removeClass("hidden")
        """.format(MealPal.SELECTORS["time_li"]))
        time.sleep(self.wait_time)
        time_li = self.get_elem("time_li")
        time_li.click()
    def reserve(self):
        btn = self.get_elem("reserve")
        btn.click()
        time.sleep(self.wait_time)
    def end(self):
        self.driver.quit()

if __name__=="__main__":
    driver = webdriver.Chrome()
    username = os.getenv("username")
    password = os.getenv("password")
    search = os.getenv("search")
    print """Ordering for
        username: {}
        password: {}
        search: {}
    """.format(username, password, search)
    actor = MealPal(driver, username, password)
    actor.login()
    actor.search(search)
    actor.select_first()
    actor.reserve()
    actor.end()