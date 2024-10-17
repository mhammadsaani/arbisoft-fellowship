from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from .spiders.constants import PUBLISH_DATE_ID


def extract_publish_date(selector):
    date_parts = [
        part.strip() 
        for part in selector.css(PUBLISH_DATE_ID).getall()
        if part.strip() not in ['', '·']
    ]
    if len(date_parts) == 1:
        date_parts = [part for part in date_parts[0].split() if part.strip() not in ['', '·']]
    return '-'.join(date_parts)



def complete_link(href):
    BASE_URL = 'https://www.educative.io'
    return BASE_URL + href


class EducativeItem(Item):
    blog_title = Field(
        output_processor=TakeFirst()
    )
    blog_link = Field(
        input_processor=MapCompose(complete_link),
        output_processor=TakeFirst()
    )
    blog_summary = Field(
        output_processor=TakeFirst()
    )
    blog_image_link = Field(
        input_processor=MapCompose(complete_link),
        output_processor=TakeFirst()
    )
    blog_publish_date = Field(
        input_processor=MapCompose(extract_publish_date),
        output_processor=TakeFirst()
    )
    author_name = Field(
        output_processor=TakeFirst()
    )
