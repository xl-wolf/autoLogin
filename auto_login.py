from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver import ActionChains
import computeLeft
import os


screen_shot_dir = "./screen_shot_dir/"

if not os.path.exists(screen_shot_dir):
    os.makedirs(screen_shot_dir)


def inupt_characters(characters, input_ele):
    for char in characters:
        input_ele.send_keys(char)
        sleep(0.1)


def login():
    javascript = 'window.location.href="https://upass.10jqka.com.cn/login"'
    driver.execute_script(javascript)
    sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, '//*[@id="to_account_login"]/a').click()
    uname_ele = driver.find_element(By.XPATH, '//*[@id="uname"]')
    pwd_ele = driver.find_element(By.XPATH, '//*[@id="passwd"]')
    uname = '11111111111111'
    password = '3333333333'
    inupt_characters(uname, uname_ele)
    inupt_characters(password, pwd_ele)
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="account_pannel"]/div[4]').click()
    sleep(2)
    slide()


def slide():
    slide_btn = driver.find_element(By.XPATH, '//*[@id="slicaptcha-block"]')
    # 截图保存为target.png
    slide_btn.screenshot(r''+screen_shot_dir+'target.png')
    # 使用js隐藏方块
    js = "document.getElementById('slicaptcha-block').style['visibility'] = 'hidden'"
    driver.execute_script(js)
    sleep(1)
    bg_img = driver.find_element(By.XPATH, '//*[@id="slicaptcha-img"]')
    # 截图保存为background.png
    bg_img.screenshot(r''+screen_shot_dir+'background.png')
    # 截图后使用js显示方块
    js = "document.getElementById('slicaptcha-block').style['visibility'] = 'visible'"
    driver.execute_script(js)
    sleep(2)

    distance = computeLeft.detect_displacement(r''+screen_shot_dir+'target.png', r''+screen_shot_dir+'background.png')
    # 点击滑块
    slider = driver.find_element(By.XPATH, '//*[@id="slider"]')
    zero_distance = distance*0.1
    first_distance = distance*0.1
    second_distance = distance*0.7
    third_distance = distance*0.1
    actionChains = ActionChains(driver)
    actionChains.click_and_hold(slider).perform()

    actionChains.move_by_offset(zero_distance, 1).perform()
    sleep(0.2)
    actionChains.move_by_offset(first_distance, 0).perform()
    sleep(0.1)
    actionChains.move_by_offset(second_distance, -1).perform()
    sleep(0.2)
    actionChains.move_by_offset(third_distance, 1).perform()
    sleep(2)

    actionChains.release().perform()


driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 隐式等待时间10s
driver.maximize_window()

login()
sleep(300)
driver.quit()
