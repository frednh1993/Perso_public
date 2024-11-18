from pathlib import Path
import scrapy




class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]


    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        # # 1) Save each url response in file.
        # # Exemple : https://example.com/category/item/12345 (response.url) -> item (page).
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # # Write raw response content into the file.
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        # 2) Extract the specified responses.
        for quote in response.css("div.quote"): 
            yield {
                "text" : quote.css("span.text::text").get(),
                "author" : quote.css("small.author::text").get(),
                "tags" : quote.css("div.tags a.tag::text").getall(),
            }

        # # a)
        # next_page = response.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # # b)
        # next_page = response.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # c)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            for href in response.css("ul.pager a::attr(href)"):
                yield response.follow(href, callback=self.parse)
