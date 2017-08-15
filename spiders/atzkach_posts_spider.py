# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup


class BechadreiPostSpider(scrapy.Spider):
    name = 'bechadrei_post_spider'
    allowed_domains = [
    'bhol.co.il',
    ]
    start_urls = ['http://www.bhol.co.il/forums/forum.asp?forum_id=1364']

    def parse(self, response):

        #get each cluster url
        table = response.css('.block_m tr')
        for index_row in table:
            cluster_page = index_row.css('a.par2::attr(href)').extract_first()
            #cluster_page = index_row.css('.par2 td:nth-child(4) span:nth-child(1) a::attr(href)').extract_first()
            yield response.follow(cluster_page, callback=self.parse_clusters)

        #get next index page
        next_page = response.xpath ('//img[@src="images/arright.gif"]/../@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_clusters(self, response):

        # loop through teguvos to get their information
        amount_of_teguvos = len(response.css('td.main_td2_alt[rowspan="2"], td.main_td2[rowspan="2"]'))
        for i in range(amount_of_teguvos):

            #using BeautifulSoup to somewhat clean up each teguva
            soup = BeautifulSoup(response.css('td.main_td2_alt[rowspan="2"], td.main_td2[rowspan="2"]')[i].extract(), "lxml")
            #put title in var so we can use it later because otherwise it would get cleaned out in next step
            soup_title = soup.u.get_text()
            #put signature in var so we can use it later and delete it in next step
            signature =''
            try:
                signature = soup.find(style="font-size: 10pt; color: silver").find_next_sibling().get_text(strip=True)
            except:
                pass
            try:
                for match in soup.findAll(style="font-size: 10pt; color: silver"):
                    match.decompose()
            except:
                pass
            #clean up tegva
            for match in soup.findAll(["html", "body","table", "div", "b", "u", "tr", "td", "font", "span", "b"]):
                match.replaceWithChildren()
            #for match in soup.findAll(dir="RTL"):
            #    match.unwrap()
            #remove devach links
            for match in soup.findAll(href="javascript:void(0);"):
                match.decompose()
            #remove signature

            # remove title from post
            for match in soup.findAll(["b", "u"]):
                match.decompose()


            yield {
                'cluster_title' : response.css ('h1.nav::text').extract_first(),  #this is the cluster title
                'cluster_id' : re.findall('(?<=topic_id=)(.*?)(?=&forum_id)', response.url), #cluster_id so we can later reconstruct clusters by this id
                'datetime' : ''.join(response.css('.main_td1 td:nth-child(1)::text, .main_td1_alt td:nth-child(1)::text')[i].re('[0-9/\xa0]')), # this gives the date in dd/mm/yyyy HHMM
                'author' :  response.css ('script').re('(?<=.addItem\("1", ")(.*?)(?=", "", "", true, null,)')[i],
                'author_id': response.css ('script').re('(?<=search_user.asp\?userid=)(.*)(?=")')[i],  #get userid for post
                'post_title' : str(soup_title),#this will be same as cluster_title for first post in cluster, will get post title if exists, othrwise will be empty string
                'post_content' : str(soup),
                'signature' : str(signature),
                }






        next_page = response.xpath ('//img[@alt="לדף הבא"]/../@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_clusters)
