import time
import asyncio
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from constants import ALLOWED_CATEGORIES_DICT


async def get_product_link(driver):
    try:
        objects = driver.find_elements(By.CLASS_NAME, 'item-collection.hover-change')
        time.sleep(2)
        tags = objects[-1].find_elements(By.CLASS_NAME, 'tile-title')
        links_container = []
        for tag in tags:
            link = tag.get_attribute('href')
            links_container.append(link)        
        return links_container
    
    except Exception as e:
        print(e)
        return None


async def pagination(driver):
    pagination = driver.find_elements(By.CLASS_NAME, 'page-controls.page-next')
    btn_pagi = pagination[1]
    for _ in range(1, 3):
        btn_pagi.click()
        time.sleep(1)
    return await get_product_link(driver)


async def open_page(category):
    driver = await create_driver()
    if driver: 
        try:
            driver.get(url = f"{ALLOWED_CATEGORIES_DICT[category]}")
            await asyncio.sleep(2)
            return await pagination(driver)
        except Exception as e:
            print(e)
            return None
    

async def create_driver():
    try: 
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        driver.implicitly_wait(5)
        return driver
    except Exception as e:
        print(e)
        return None