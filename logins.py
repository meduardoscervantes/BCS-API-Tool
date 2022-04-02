import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup as bs
import config


def bcs_login():
    url = "https://bootcampspot.com/"

    driver = webdriver.Firefox()
    driver.maximize_window()

    # Login to BCS
    driver.get(url + "login")
    WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="emailAddress"]')))
    email = driver.find_element(By.XPATH, '//*[@id="emailAddress"]')
    pw = driver.find_element(By.XPATH, '//*[@id="password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="root"]/section/div/div[2]/button')

    email.send_keys(config.EMAIL)
    pw.send_keys(config.BCS_PASSWORD)
    submit.click()

    # Navigate to the students tab and find the name of current active students
    WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/nav/div[2]/nav/ul/li[8]/a')
        )
    )
    driver.get(url + 'students')
    WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/main/div/section')
        )
    )
    soup = bs(driver.page_source, 'html.parser')
    student_cards = soup.findAll('div', class_='col-xs-12 col-sm-4 col-md-3')
    os.chdir('data')
    pd.DataFrame(
        {
            'name': [x.getText() for x in student_cards]
        }
    ).to_csv('active_students.csv', index=False)
    os.chdir('..')

    # Go back to main screen to join the class #
    driver.get(url)
    WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "main-content"] / div / section / div / div[2] / div / div / div / a')
        )
    )
    join_class = driver.find_element(By.XPATH,
                                     '// *[ @ id = "main-content"] / div / section / div / div[2] / div / div / div / a')
    join_class.click()

def gitlab_login():
    url = "https://utsa.bootcampcontent.com/users/sign_in"

    driver = webdriver.Firefox()
    driver.get(url)

    WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="user_login"]')))
    email = driver.find_element(By.XPATH, '//*[@id="user_login"]')
    pw = driver.find_element(By.XPATH, '//*[@id="user_password"]')
    submit = driver.find_element(By.XPATH, '//*[@id="new_user"]/div[5]/input')

    email.send_keys(config.EMAIL)
    pw.send_keys(config.GITLAB_PASSWORD)
    submit.click()

    WebDriverWait(driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[3]/main/div[5]/ul/li/div[2]/div[1]/div/h2/a/span/span[1]')))
    home = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/main/div[5]/ul/li/div[2]/div[1]/div/h2/a/span/span[1]')
    home.click()


def initial_login():
    bcs_login()
    # gitlab_login()

    quit("Welcome To another class session!")


initial_login()
# get_active_students()