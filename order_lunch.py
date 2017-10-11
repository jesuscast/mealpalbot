from selenium import webdriver
from MealPal import MealPal
import os

if __name__=="__main__":
    driver = webdriver.Chrome()
    username = os.getenv("username")
    password = os.getenv("password")
    search = os.getenv("search")
    print """Ordering for
        username: {}
        search: {}
    """.format(username, search)
    actor = MealPal(driver, username, password)
    actor.login()
    actor.search(search)
    actor.select_first()
    actor.reserve()
    actor.end()