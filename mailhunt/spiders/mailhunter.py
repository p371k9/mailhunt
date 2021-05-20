# -*- coding: utf-8 -*-
import scrapy
import re
from mailhunt.items import MailhuntItem
from urllib.parse import urlparse
#from scrapy.shell import inspect_response

def getUrls(s):
    if len(s) == 0:
        return ['']
    if s[0] == '@':
        with open(s[1:]) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content
    else: 
        return [s]

class MSpider(scrapy.Spider):
    name = 'mailhunter'
    #allowed_domains = ['munkaspart.hu']
    #start_urls = ['https://munkaspart.hu']
    
    #allowed_domains = ['munkaspart.hu', 'hotelbenczur.hu', 'amiidonk.hu']
    start_urls = ['https://munkaspart.hu/kapcsolat/kapcsolat', 'http://www.hotelbenczur.hu', 'http://amiidonk.hu', 'http://nincsilyen.hu', 'http://www.konyveles-miskolcon.hu/']    
    
    def __init__(self, url=None, *args, **kwargs):
        #super(Mh1Spider, self).__init__(*args, **kwargs)
        if url != None:
            self.start_urls = getUrls(url)
            #o = urlparse(url)
            #self.allowed_domains = [o.hostname]

    def parse(self, response):
        def search_in_pg():
            match = re.search(r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', response.text)
            if (match):
                self.logger.info('************************')
                return match.group()
            else:
                return ''

        #inspect_response(response, self)               
        mail = search_in_pg()
        if mail != '':
            doc = MailhuntItem()
            doc['url'] = response.url
            doc['mail'] = mail
            yield doc
            return
            
        if 'links' in response.meta:
            if len(response.meta['links']) > 0:
                nl = response.meta['links'][0]
                response.meta['links'].pop(0)
                yield response.follow(url=nl, meta={'links': response.meta['links']}, callback=self.parse)                 
        else:
            links = []
            for x in response.xpath('//a/@href'):            
                href = x.extract()            
                for y in self.settings.get('RLS'): 
                    if y in href:
                        links.append(href)
            if len(links) > 0:
                nl = links[0]
                links.pop(0)
                yield response.follow(url=nl, meta={'links': links}, callback=self.parse) 
                         
