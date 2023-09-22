import scrapy


class PropertySpider(scrapy.Spider):
    name = "emlak_az"
    allowed_domains = ["emlak.az"]
    start_urls = ["https://emlak.az/elanlar/?ann_type=1&sort_type=0&page=595&page=1"]

    def parse(self, response):
        hrefs = response.xpath('//a[@class="m-trig" and @style="display:none;"]/@href').getall()

        for href in hrefs:
            yield response.follow(href, callback=self.parse_property, meta={"href": href})

        # Extract the pagination link and follow it
        next_page_link = response.xpath('//a[contains(text(), "Növbəti")]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_property(self, response):
        href = response.request.meta['href'],
        id = response.xpath('//p[@class="pull-right"]/b/text()').get()
        info = response.xpath('//h1[@class="title"]/text()').getall()
        price = response.xpath('//div[@class="price"]/span[@class="m"]/text()').get()
        views_count = response.xpath('//span[@class="views-count"]/strong/text()').get()
        date = response.xpath('//span[@class="date"]/strong/text()').get()
        description = response.xpath('//div[@class="desc"]/p/text()').get()
        area = response.xpath('//dl[@class="technical-characteristics"]/dd[2]/text()').get()
        room_count = response.xpath('//dl[@class="technical-characteristics"]/dd[3]/text()').get()
        flat = response.xpath('//dl[@class="technical-characteristics"]/dd[4]/text()').get()
        repair_type = response.xpath('//dl[@class="technical-characteristics"]/dd[5]/text()').get()
        document_type = response.xpath('//dl[@class="technical-characteristics"]/dd[6]/text()').get()
        property_type = response.xpath('//dl[@class="technical-characteristics"]/dd[1]/text()').get()
        seller_name = response.xpath('//p[@class="name-seller"]/text()[normalize-space()]').get()
        seller_categoey = response.xpath('//p[@class="name-seller"]/span[1]/text()').get()
        phone_numbers = response.xpath('//div[@class="silver-box"]/p[@class="phone"]/text()').get()

        yield {
            "href": href,
            "id": id,
            "info": info,
            "views_count": views_count,
            "date": date,
            "description": description,
            "price": price,
            "area": area,
            "room_count": room_count,
            "flat": flat,
            "repair_type": repair_type,
            "document_type": document_type,
            "property_type": property_type,
            "seller_name": seller_name,
            "seller_categoey": seller_categoey,
            "phone_numbers": phone_numbers
        }