import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from babilou.items import BabilouItem
from scrapy.shell import inspect_response
from scrapy.selector import Selector
import json

class CrechesSpider(scrapy.Spider):
    name = 'creches'
    allowed_domains = ['babilou.fr']
    start_urls = ['http://babilou.fr/']

    def __init__(self):
        self.url_template = 'https://www.babilou.fr/trouvez-une-creche?location_place=Paris%2013%2C%20Paris%2C%20France&location_lat=48.8261675&location_lng=2.3598969&opening_hour=All&closing_hour=All&field_micro=All&field_outdoorspace=All&opening_hour_list=All&opening_hour_radio_list=All&closing_hour_list=All&closing_hour_radio_list=All&page={}'
        self.url_additional_template = 'https://www.babilou.fr/creches/{}'

    def start_requests(self):
        yield Request(
            self.url_template.format(1)
        )
    def parse(self,response):   
        total_pages = int(response.xpath('//li[@class="pager__item pager__item--last"]/a/@href').get().split('=')[-1]) + 1
        for page in range(total_pages):
            yield Request(
                self.url_template.format(page),
                callback = self.parse_products
            )


    def parse_products(self, response):
        # extract infos 
        creches = response.css('div.nursery__content-wrapper')
        for crech in creches :
            loader = ItemLoader(BabilouItem(),crech)
            loader.add_css('name','h2.nursery__title span::text')
            loader.add_css('crech_type','span.partner::text')
            loader.add_css('address','span.address-line1::text')
            loader.add_css('postal_code','span.postal-code::text')
            loader.add_css('image','div.nursery__img img::attr(src)')
            loader.add_value('url','https://www.babilou.fr' + crech.css('div.nursery__actions a::attr(href)').get())
            yield Request(
                loader._values['url'][0],
                callback=self.parse_additional_infos,
                meta={
                    'loader':loader
                }
            )

    def parse_additional_infos(self,response):
        loader = response.meta.get('loader')
        #inspect_response(response, self)
        loader.add_value('description',self.get_description(response))
        loader.add_value('format',response.xpath('(//div[@class="nursery__micro-label"])[1]//text()').get())
        loader.add_value('capacity',response.xpath('(//div[@class="nursery__capacity-item"])[1]/text()').get())
        loader.add_value('size',response.xpath('(//div[@class="nursery__surface-item"])[1]/text()').get())
        loader.add_value('benefits',response.xpath('(//div[@class="nursery__plus-content"])[1]/div/div/text()').getall())
        loader.add_value('access',response.xpath('(//div[@class="nursery__age-range"]//strong/text())[1]').get())
        loader.add_value('cd',response.xpath('//span[@class="locality"]/text()').get())
        loader.add_value('open_hour',self.get_open_hour(response))
        yield loader.load_item()

    def get_description(self,response):
        try :
            data = json.loads(response.xpath('//script[@type="application/vnd.drupal-ajax"]/text()')[-2].get())[0]['data']
        except KeyError :
            return 'no description'
        selector = Selector(text=data)
        return selector.xpath('string(//div[@class="cost-simulator__PAJE"])').get()

    def get_open_hour(self,response):
        open_hours =  {
            label:hour for label,hour in zip(
                response.xpath('(//div[@class="office-hours"])[1]//span[@class="office-hours__item-label"]/text()').getall(),
                response.xpath('(//div[@class="office-hours"])[1]//span[@class="office-hours__item-slots"]/text()').getall()
            )
        }
        if open_hours :
            return open_hours
        else:
            return {
            response.xpath('//div[@class="office-hours__label"]/text()').get():response.xpath('//div[@class="office-hours__value"]/text()').get()
        }


