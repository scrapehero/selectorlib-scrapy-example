# -*- coding: utf-8 -*-
import scrapy
import os 
import selectorlib
from selectorlib.formatter import Formatter

class Price(Formatter):
    def format(self, text):
        price = text.replace('£','').strip()
        return float(price)

class ScrapemeSpider(scrapy.Spider):
    name = 'scrapeme_with_formatter'
    allowed_domains = ['scrapeme.live']
    start_urls = ['http://scrapeme.live/shop/']
    # Create Extractor for listing page
    listing_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../selectorlib_yaml/ListingPage.yml'))
    # Create Extractor for product page
    product_page_extractor = selectorlib.Extractor.from_yaml_file(os.path.join(os.path.dirname(__file__),'../selectorlib_yaml/ProductPage_with_Formatter.yml'),formatters = [Price])

    def parse(self, response):
        # Extract data using Extractor
        data = self.listing_page_extractor.extract(response.text)
        if 'next_page' in data: 
            yield scrapy.Request(data['next_page'],callback=self.parse)
        for p in data['product_page']:
            yield scrapy.Request(p,callback=self.parse_product)
    
    def parse_product(self, response):
        # Extract data using Extractor
        product = self.product_page_extractor.extract(response.text)
        if product: 
            yield product