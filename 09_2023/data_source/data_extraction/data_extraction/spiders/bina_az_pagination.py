import scrapy


class BinaAzPaginationSpider(scrapy.Spider):
    name = "bina_az_pagination"
    allowed_domains = ["bina.az"]
    start_urls = ["https://bina.az/baki/kiraye/menziller?page=1"]

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
            'id': response.css('.product-actions__id::text').get(),
            'view': response.css('span.product-statistics__i-text::text').getall(),
            'updated': response.css('span.product-statistics__i-text::text').get(),
            'title': response.css('.product-title::text').get(),
            'seller_type': response.css('.product-owner__info-region::text').get(),
            'name': response.css('.product-owner__info-name::text').get(),
            'phone': response.css('.product-phones__btn-value::text').get(),
            'url': response.url,
            'price': response.css('.price-val::text').get(),
            'currency': response.css('.price-cur::text').get(),
            'location': response.css('div.product-map__left.bz-d-flex.bz-align-center div::text').get(),
            'address': response.css('li.product-extras__i > a::text').get(),
            'address_all': response.css('li.product-extras__i > a::text').getall(),
            'description': response.css('.product-description__content p::text').getall(),
            'building_type': response.css("span.product-properties__i-value::text").get(),
            'all_data': response.css("span.product-properties__i-value::text").getall(),
        }
