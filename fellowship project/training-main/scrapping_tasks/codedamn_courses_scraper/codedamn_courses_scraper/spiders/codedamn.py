import time
import scrapy
from .constants import LOGIN_PAGE_URL
from .utils import (
    login, open_chrome, expand_course_sections, get_video_links, open_course
)


class CodedamnSpider(scrapy.Spider):
    name = 'codedamn'
    
    def start_requests(self):
        yield scrapy.Request(
            LOGIN_PAGE_URL,
            callback=self.scrap_codedamn
        )
        
    def scrap_codedamn(self, response):
        driver = open_chrome(response.url)
        login(driver)
        time.sleep(20)
        open_course(driver)
        expand_course_sections(driver)
        video_info = get_video_links(driver, driver.page_source, response)
        time.sleep(60)
        for video_title, video_link in video_info.items():
            yield {
                video_title: video_link
            }
        driver.close()
