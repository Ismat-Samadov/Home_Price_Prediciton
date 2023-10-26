import scrapy
class BinaAzPaginationSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["bina.az"]
    start_urls = ["https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?page=1"]

    def parse(self, response):
        links = response.css('.item_link::attr(href)').getall()

        for link in links:
            yield response.follow(link, self.parse_item, meta={'link': link})

        next_page_link = response.css('span.next a::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, self.parse)

    def parse_item(self, response):
        self.logger.info('Parsing page: %s', response.url)
        yield {
            'id'            : response.css('.product-actions__id::text').get(),
            'link'          : response.url,
            'view'          : response.css('span.product-statistics__i-text::text').getall(),
            'updated'       : response.css('span.product-statistics__i-text::text').get(),
            'title'         : response.css('.product-title::text').get(),
            'seller_type'   : response.css('.product-owner__info-region::text').get(),
            'price'         : response.css('.price-val::text').get(),
            'currency'      : response.css('.price-cur::text').get(),
            'description'   : response.css('.product-description__content p::text').getall(),
            'category'      : response.css('label.product-properties__i-name:contains("Kateqoriya") + span.product-properties__i-value::text').get(),
            'flat_number'   : response.css('label.product-properties__i-name:contains("Mərtəbə") + span.product-properties__i-value::text').get(),
            'area'          : response.css('label.product-properties__i-name:contains("Sahə") + span.product-properties__i-value::text').get(),
            'room_count'    : response.css('label.product-properties__i-name:contains("Otaq sayı") + span.product-properties__i-value::text').get(),
            'documents'     : response.css('label.product-properties__i-name:contains("Çıxarış") + span.product-properties__i-value::text').get(),
            'is_repair'     : response.css('label.product-properties__i-name:contains("Təmir") + span.product-properties__i-value::text').get(),

        }
