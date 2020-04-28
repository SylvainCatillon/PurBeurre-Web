from django.urls import reverse
from django.contrib.auth.models import User

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_user_in(driver, server_url):
    """Log a user in using a selenium driver"""
    user_info = {
        "username": "test_user",
        "email": "user@test.com",
        "password": "test_user_password",
        "first_name": "Paul"}
    user = User.objects.create_user(**user_info)
    driver.get(server_url+reverse("accounts:login"))
    username = driver.find_element_by_name("username")
    username.send_keys(user_info["username"])
    password = driver.find_element_by_name("password")
    password.send_keys(user_info["password"])
    driver.find_element_by_xpath(
        "//form[@id='login_form']/button[@type='submit']").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myAccount")))
    return user
