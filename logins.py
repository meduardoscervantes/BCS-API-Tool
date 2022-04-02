from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import config


def bcs_login():
    url = "https://bootcampspot.com/login"

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)

    email = WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="emailAddress"]')))
    email = driver.find_element(By.XPATH, '//*[@id="emailAddress"]')
    pw = driver.find_element(By.XPATH, '//*[@id="password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="root"]/section/div/div[2]/button')

    email.send_keys(config.EMAIL)
    pw.send_keys(config.BCS_PASSWORD)
    submit.click()

    # Todo:
    #   get all of current active students.

    join_class = WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "main-content"] / div / section / div / div[2] / div / div / div / a')))
    join_class = driver.find_element(By.XPATH,
                                     '// *[ @ id = "main-content"] / div / section / div / div[2] / div / div / div / a')
    join_class.click()

def gitlab_login():
    url = "https://utsa.bootcampcontent.com/users/sign_in"

    driver = webdriver.Firefox()
    driver.get(url)

    email = WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="user_login"]')))
    email = driver.find_element(By.XPATH, '//*[@id="user_login"]')
    # email = driver.find_element(By.XPATH, '//*[@id="emailAddress"]')
    pw = driver.find_element(By.XPATH, '//*[@id="user_password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="new_user"]/div[5]/input')

    email.send_keys(config.EMAIL)
    pw.send_keys(config.GITLAB_PASSWORD)
    submit.click()

    home = WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[3]/main/div[5]/ul/li/div[2]/div[1]/div/h2/a/span/span[1]')))
    home = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/main/div[5]/ul/li/div[2]/div[1]/div/h2/a/span/span[1]')
    home.click()


def initial_login():
    bcs_login()
    gitlab_login()

    quit("Welcome To another class session!")

def get_active_students():
    """
    TODO: Make a selenium call to the students page and find the name of the students listed
    :return:
    """
    url = "https://bootcampspot.com/login"

    driver = webdriver.Firefox()
    driver.get(url)

    email = WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="emailAddress"]')))
    email = driver.find_element(By.XPATH, '//*[@id="emailAddress"]')
    pw = driver.find_element(By.XPATH, '//*[@id="password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="root"]/section/div/div[2]/button')

    email.send_keys(config.EMAIL)
    pw.send_keys(config.BCS_PASSWORD)
    submit.click()

    driver.get("https://bootcampspot.com/students")

initial_login()
# get_active_students()