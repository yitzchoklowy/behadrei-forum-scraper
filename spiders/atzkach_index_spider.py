# -*- coding: utf-8 -*-
import scrapy


class BechadreiIndexSpider(scrapy.Spider):
    name = 'bechadrei_index_spider'
    allowed_domains = [
    'bhol.co.il',
    ]
    start_urls = ['http://www.bhol.co.il/forums/forum.asp?forum_id=1364']

    def parse(self, response):

        #get each cluster index listing with info from index pages
        table = response.css('.block_m tr')
        for index_row in table:
            yield {
                    'cluster_title' : index_row.css ('td:nth-child(4) a::text').extract_first(),
                    'cluster_author' : index_row.css ('td:nth-child(4) span:nth-child(3) a::text').extract(),
                    'replies_number' : index_row.css ('td:nth-child(3) span::text').extract(),
                    'views_number' : index_row.css ('td:nth-child(2) span::text').extract(),
                    'last_reply_author' : index_row.css ('td .par2 a::text').extract_first(),
                    'last_reply_time' : index_row.css ('td .par2_sub::text').extract_first(),
                    'cluster_url' : index_row.css ('td:nth-child(4) a::attr(href)').extract_first(),
                    'cluster_id' : index_row.css ('.par2 a::attr(href)').re('(?<=topic_id=)(.*)')
                    }

        #get the next page of each page
        next_page = response.css('.par2 a::attr(href)')[-1].extract()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
