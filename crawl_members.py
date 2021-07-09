from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from numpy.random import randint
from time import sleep

def init_driver(file_path):
    chrome_options = webdriver.ChromeOptions()
    # Save account
    chrome_options.add_argument(
        "user-data-dir="+file_path
    )
    # Disabel notification chrome
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('./chromedriver', chrome_options= chrome_options)
    # Login facebook
    driver.get('https://facebook.com')
    sleep(randint(3,5))
    return driver

def scroll_down(n):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(randint(7,10))

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or n == 0:
            break
        last_height = new_height
        n -= 1

def crawl_link_user():
    link_user = []
    span = driver.find_elements_by_class_name("nc684nl6")
    for s in span:
        try:
            a = s.find_element_by_tag_name('a')
            link = a.get_attribute('href')
            link_user.append(link.split('/')[-2] + '\n')
        except:
            pass
    return link_user

if __name__ == '__main__':
    # Get list vietnamese name
    with open('vietnamese_name.txt', 'r') as f:
        vietnamese_name = f.readlines()
    vietnamese_name = [name.replace('\n', '') for name in vietnamese_name]

    # Open facebook
    driver = init_driver('profile')
    driver.get('https://www.facebook.com/groups/quantrimang365/members')
    sleep(randint(3,5))

    # search
    link = []
    id = 1
    for name in vietnamese_name:
        search_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Tìm kiếm thành viên nhóm"]')))  
        search_name.clear()  
        search_name.send_keys(name)
        sleep(randint(3,5))
        scroll_down(1000000)
        link = crawl_link_user()
        with open('save/link_user_{}.txt'.format(id), 'w+') as f:
            f.writelines(link)
        id += 1
    
    
    driver.close()