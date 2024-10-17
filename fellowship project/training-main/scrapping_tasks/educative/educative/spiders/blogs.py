import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from playwright._impl._api_types import TimeoutError
from .constants import (
    AUTHOR_NAME, AUTHOR_NAME_CSS, BLOG_ID, BLOG_IMAGE_LINK, BLOG_LINK, BLOG_PUBLISH_DATE,
    BLOG_SUMMARY, BLOG_TITLE, BLOGS_CLASS, BLOGS_PER_PAGE, IMAGE_LINK_CSS, LINK_CSS,
    PLAYWRIGHT, PLAYWRIGHT_PAGE, PUBLISH_DATE_CSS, SCROLL_HEIGHT, SUMMARY_CSS,
    TITLE_CSS, TOTAL_PAGES, URL
)
from ..items import EducativeItem


class EducativeBlogScraper(scrapy.Spider):
    name = 'educative'
    
    def start_requests(self):
        yield scrapy.Request(
            URL,
            meta=PLAYWRIGHT,
            errback=self.close_page
        )

    async def parse(self, response):
        page = response.meta[PLAYWRIGHT_PAGE]
        for page_number in range(TOTAL_PAGES):
            try:
                blog_number = page_number * BLOGS_PER_PAGE
                await page.wait_for_selector(f'{BLOG_ID}{blog_number}')
                await page.evaluate(SCROLL_HEIGHT)
            except TimeoutError:
                break
        html_content = await page.content()
        await page.close()
        return self.extract_blogs(html_content)
    
    def extract_blogs(self, html_content):
        response = Selector(text=html_content)
        blogs = response.css(BLOGS_CLASS)
        for blog in blogs:
            loader = ItemLoader(item=EducativeItem())
            loader.add_value(BLOG_TITLE, blog.css(TITLE_CSS).get())
            loader.add_value(BLOG_LINK, blog.css(LINK_CSS).get())
            loader.add_value(BLOG_SUMMARY, blog.css(SUMMARY_CSS).get())
            loader.add_value(BLOG_IMAGE_LINK, blog.css(IMAGE_LINK_CSS).get())
            loader.add_value(BLOG_PUBLISH_DATE, blog.css(PUBLISH_DATE_CSS))
            loader.add_value(AUTHOR_NAME, blog.css(AUTHOR_NAME_CSS).get())
            yield loader.load_item()
                  
    async def close_page(self, error):
        page = error.request.meta[PLAYWRIGHT_PAGE]
        print("The reason page was closed is ", error)
        await page.close()
