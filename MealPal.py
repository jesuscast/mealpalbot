from selenium.common.exceptions import NoSuchElementException
from DriverWrapper import DriverWrapper
import time

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
        """)
        time.sleep(self.wait_time)
        time_li = self.get_elem("time_li")
        time_li.click()
    def reserve(self):
        btn = self.get_elem("reserve")
        btn.click()
        time.sleep(self.wait_time)
    def end(self):
        self.driver.quit()