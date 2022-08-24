from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver import ActionChains
import compute_left
import os


login_success = False


screen_shot_dir = "./screen_shot_dir/"


def make_image_dir():
    if not os.path.exists(screen_shot_dir):
        os.makedirs(screen_shot_dir)


def inupt_characters(characters, input_ele):
    for char in characters:
        input_ele.send_keys(char)
        sleep(0.05)


def login(uname, password):
    javascript = 'window.location.href="https://upass.10jqka.com.cn/login"'
    driver.execute_script(javascript)
    sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.XPATH, '//*[@id="to_account_login"]/a').click()
    uname_ele = driver.find_element(By.XPATH, '//*[@id="uname"]')
    pwd_ele = driver.find_element(By.XPATH, '//*[@id="passwd"]')
    inupt_characters(uname, uname_ele)
    inupt_characters(password, pwd_ele)
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="account_pannel"]/div[4]').click()
    sleep(1)
    while not login_success:
        slide()


def slide():
    try:
        user_avatar_ele = driver.find_element(
            By.XPATH, '//*[@id="header_logined"]/a/img')
        if(bool(user_avatar_ele)):
            global login_success
            login_success = True
            print("登录成功！")
            return
    except:
        print("未登录！")
        pass
    slide_btn = driver.find_element(By.XPATH, '//*[@id="slicaptcha-block"]')
    # 截图保存为target.png
    slide_btn.screenshot(r''+screen_shot_dir+'target.png')
    # 使用js隐藏方块
    js = "document.getElementById('slicaptcha-block').style['visibility'] = 'hidden'"
    driver.execute_script(js)
    bg_img = driver.find_element(By.XPATH, '//*[@id="slicaptcha-img"]')
    # 截图保存为background.png
    bg_img.screenshot(r''+screen_shot_dir+'background.png')
    # 截图后使用js显示方块
    js = "document.getElementById('slicaptcha-block').style['visibility'] = 'visible'"
    driver.execute_script(js)
    sleep(1)

    distance = compute_left.detect_displacement(
        r''+screen_shot_dir+'target.png', r''+screen_shot_dir+'background.png')
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
    actionChains.move_by_offset(third_distance, 0).perform()
    sleep(1)

    actionChains.release().perform()


def create_options(option_obj):
    # 开发者模式 -- 就等于是手动按下F2的效果
    option_obj.add_argument("--auto-open-devtools-for-tabs")
    # 使用无头模式
    # option_obj.add_argument('--headless')
    return option_obj


def create_chromedriver():
    options = Options()
    res_options = create_options(options)
    driver = webdriver.Chrome(executable_path='D:\chromedriver.exe',chrome_options=res_options)
    driver.implicitly_wait(10)  # 隐式等待时间10s
    driver.maximize_window()
    return driver


def screenshotCanvas():
    javascript = 'window.open("https://t.10jqka.com.cn/portfolioFront/detail.html?id=75","_blank")'
    driver.execute_script(javascript)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(5)
    driver.set_window_size(946, 1200)
    driver.refresh()
    sleep(5)
    canvas = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/canvas')
    canvas.screenshot(r''+screen_shot_dir+'canvas.png')


driver = create_chromedriver()


def main():
    uname = 'xyja51'
    password = 'sns654321'
    login(uname, password)
    if(login_success):
        # 登录成功后再过60s退出浏览器
        screenshotCanvas()
        sleep(60)
        driver.quit()


if(__name__ == '__main__'):
    make_image_dir()
    main()
