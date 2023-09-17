import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class MainSpider(CrawlSpider):
    name            = 'bina_az'
    allowed_domains = ['bina.az']
    start_urls      = ['https://bina.az/items/']

    rules = (
               Rule(LinkExtractor( allow    =  ('/items/')),
                                   callback =  'parse_item',
                                   follow   =  True
                   ),
            )

    def parse_item(self, response):
        self.logger.info('Parsing page: %s', response.url)
        yield {
            'id'                   : response.css('.product-actions__id::text').get(),
            'view'                 : response.css('span.product-statistics__i-text::text').getall(),
            'updated'              : response.css('span.product-statistics__i-text::text').get(),
            'title'                : response.css('.product-title::text').get(),
            'seller_type'          : response.css('.product-owner__info-region::text').get(),
            'name'                 : response.css('.product-owner__info-name::text').get(),
            'phone'                : response.css('.product-phones__btn-value::text').get(),
            'url'                  : response.url,
            'price'                : response.css('.price-val::text').get(),
            'currency'             : response.css('.price-cur::text').get(),
            'location'             : response.css('.product-map__left bz-d-flex bz-align-center::text').get(),
            'address'              : response.css('.product-extras__i::text').get(),
            'address_all'          : response.css('.product-extras__i::text').getall(),
            'type'                 : response.css('table.properties td.property-value:nth-child(2)::text').get(),
            'description'          : response.css('.product-description__content p::text').getall(),

            # 'building_type'        : response.css('table.properties td.property-value:nth-child(3)::text').get(),
            # 'area'                 : response.css('table.properties td.property-value:nth-child(4)::text').get(),
            # 'room_count'           : response.css('table.properties td.property-value:nth-child(4)::text').get(),
            # 'loc_details'          : response.css('table.properties td.property-value:nth-child(4)::text').get(),

        }