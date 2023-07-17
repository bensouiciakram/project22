# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst 

class BabilouItem(scrapy.Item):
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    crech_type = scrapy.Field(
        output_processor = TakeFirst()
    )
    address = scrapy.Field(
        output_processor = TakeFirst()
    )
    postal_code = scrapy.Field(
        output_processor = TakeFirst()
    )
    image = scrapy.Field(
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        output_processor = TakeFirst()
    )
    format = scrapy.Field(
        output_processor = TakeFirst()
    )
    capacity = scrapy.Field(
        output_processor = TakeFirst()
    )
    size = scrapy.Field(
        output_processor = TakeFirst()
    )
    access = scrapy.Field(
        output_processor = TakeFirst()
    )
    size = scrapy.Field(
        output_processor = TakeFirst()
    )
    benefits = scrapy.Field(
        #output_processor = TakeFirst()
    )
    access = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    cd = scrapy.Field(
        output_processor = TakeFirst()
    )
    open_hour = scrapy.Field(
        output_processor = TakeFirst()
    )