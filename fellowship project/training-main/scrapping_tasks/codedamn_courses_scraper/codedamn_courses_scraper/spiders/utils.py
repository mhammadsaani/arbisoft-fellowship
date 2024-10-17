from scrapy.http import HtmlResponse
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from .constants import (
    COURSE_LINK, WIDTH, HEIGHT, BUTTON_ID, BASE_URL, EMAIL_ID, 
    PASSWORD_ID, COURSES_SECTION_ID,PAGE_LINK_HREF, VIDEO_SOURCE_SELECTOR,
    TITLES_CSS_SELECTOR, NEW_TAB_QUERY, UTF, EMPTY_STRING, NEW_TAB, PREVIOUS_TAB
)
from .credentials import USER, EMAIL, PASSWORD


def open_course(driver):
    driver.get(COURSE_LINK)
    time.sleep(20)
   
    
def open_chrome(url):
    driver = webdriver.Chrome()
    driver.set_window_size(WIDTH, HEIGHT)
    driver.get(url)
    time.sleep(2)
    return driver
    
        
def login(driver):
    email_input = driver.find_element(By.ID, EMAIL_ID)
    password_input = driver.find_element(By.ID, PASSWORD_ID)
    login_button = driver.find_element(
        By.CSS_SELECTOR, BUTTON_ID
    )
    email_input.send_keys(USER[EMAIL])
    password_input.send_keys(USER[PASSWORD])
    login_button.click()


def click_button(driver, value):
    try:
        button = driver.find_element(By.ID, f'{COURSES_SECTION_ID}{value}:')
        button.click()
    except NoSuchElementException:
        return


def expand_course_sections(driver):
    for number in range(8, 19, 2):
        click_button(driver, number)
        
    for asci_number in range(97, 123, 2):
        click_button(driver, chr(asci_number))


def download_video(driver, video_link):
    try:
        driver.execute_script(NEW_TAB_QUERY)
        driver.switch_to.window(driver.window_handles[NEW_TAB])
        driver.get(video_link)
        driver.close()
        driver.switch_to.window(driver.window_handles[PREVIOUS_TAB])
    except Exception:
        driver.close()
        driver.switch_to.window(driver.window_handles[PREVIOUS_TAB])
        

def process_pages(driver, pages_hrefs, response):       
    video_links = {} 
    for page_number in range(2):
        page_link = BASE_URL + pages_hrefs[page_number]
        driver.get(page_link)
        time.sleep(10)
        initial_page_source = driver.page_source
        response = HtmlResponse(url=response.url, body=initial_page_source, encoding=UTF)
        video_link = response.css(VIDEO_SOURCE_SELECTOR).get()
        titles = response.css(TITLES_CSS_SELECTOR).extract()
        title = titles[page_number].replace('\xa0\xa0', EMPTY_STRING)
        video_links[title] = video_link
        download_video(driver, video_link)
    return video_links


def get_video_links(driver, initial_page_source, response):
    course_page_html = HtmlResponse(url=response.url, body=initial_page_source, encoding=UTF)
    pages_hrefs = course_page_html.css(PAGE_LINK_HREF).extract()
    return process_pages(driver, pages_hrefs, response)
