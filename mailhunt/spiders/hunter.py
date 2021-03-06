# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from mailhunt.items import MailhuntItem
from urllib.parse import urlparse
#from w3lib.html import remove_tags
from html import unescape
#from scrapy.shell import inspect_response

class MSpider(scrapy.Spider):
    name = 'hunter'
    start_urls = ['http://nincsilyen.hu', 'http://www.konyveles-miskolcon.hu/']    
    
    def __init__(self, url=None, list=None, *args, **kwargs):        
        if url != None:
            self.start_urls = [url]            
        if list != None:
            with open(list) as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            self.start_urls = content

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta = {'start_url': url})

    def parse(self, response):
        def search_in_pg():
            #inspect_response(response, self) 
            match = re.search(r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', unescape(response.text).replace('<em>', ''))
            if (match):
                self.logger.info('************************')
                return match.group()
            else:
                return ''

                      
        mail = search_in_pg()
        if mail != '':
            doc = MailhuntItem()            
            doc['url'] = response.request.meta['start_url']
            doc['mail'] = mail
            yield doc
            return
            
        if 'links' in response.meta:
            if len(response.meta['links']) > 0:
                nl = response.meta['links'][0]
                response.meta['links'].pop(0)
                yield response.follow(url=nl, meta={'start_url': response.meta['start_url'], 'links': response.meta['links']}, callback=self.parse)                 
        else:
            links = []
            for y in self.settings.get('RLS'): 
                for x in response.xpath('//a/@href'):            
                    href = x.extract()
                    href = href.replace('\\','/')            
            
                    if y in href:
                        links.append(href)

            if len(links) > 0:
                nl = links[0]
                links.pop(0)
                yield response.follow(url=nl, meta={'start_url': response.meta['start_url'], 'links': links}, callback=self.parse)
                                        
