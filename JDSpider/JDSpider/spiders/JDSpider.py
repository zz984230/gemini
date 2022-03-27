#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = 'Kandy.Ye'
__mtime__ = '2017/4/12'
"""

import re
import logging
import json
import requests
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from JDSpider.items import *

key_word = ['book', 'e', 'channel', 'mvd', 'list']
Base_url = 'https://list.jd.com'
price_url = 'https://p.3.cn/prices/mgets?skuIds=J_'
comment_url = 'https://club.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=5&page=%s&pageSize=10'
favourable_url = 'https://cd.jd.com/promotion/v2?skuId=%s&area=1_72_2799_0&shopId=%s&venderId=%s&cat=%s'


class JDSpider(Spider):
    name = "JDSpider"
    allowed_domains = ["jd.com"]
    start_urls = [
        'https://www.jd.com/allSort.aspx'
    ]
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING

    # def parse(self, response, **kwargs):
    #     filename = "./shop.html"
    #     print(response.body)
    #     with open(filename, 'w') as f:
    #         f.write(response.body)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies={
                "pt_key": "AAJiP-cXADC8nE0KDlYj44mVslKxyLiq7ChB9gGe9Vfob2k-L9cj87jOVsQzfxR9DVL4vBjDxMg",
                "pt_pin": "mephisto_512"}, callback=self.parse_category)

    def parse_category(self, response):
        """获取分类页"""
        cookie = '__jdu=16483548252141065341557; areaId=16; PCSYCityID=CN_350000_350200_0; shshshfpb=ojJ5lyCbgY6oOFNJMEP9rZg%3D%3D; shshshfpa=5120b625-2958-07ce-f059-7adf1c1fb299-1613293234; ipLoc-djd=16-1315-3486-59641; unpl=JF8EALNnNSttC0xRBEkDGRMUTAhUW1QNH0cGPWUBXQ5QT10ATwBME0R7XlVdXhRKFR9sYRRUVFNKXQ4eASsSEXteU11bD00VB2xXXAQDGhUQR09SWEBJJVhXWloOShUCamAFZG1bS2QFGjIbFRVCX1BbVAtPFANqZwRTWVpOVAEfBCsiF3ttZFxVCk4VBV9mNVVtGh8IBx0CExQUBl1TW1QKTxIKbGMGVFhYSlMBGQcbFhRNbVVuXg; __jdv=76161171|haosou-search|t_262767352_haosousearch|cpc|42567030461_0_b640c03056d1484ea4c358b9584e3f0e|1648375723681; __jdc=122270672; ip_cityCode=1315; pinId=zaebSevvwiKZAQYe7tFpnA; pin=mephisto_512; unick=mephisto_512; ceshi3.com=103; _tp=nJatVWhdqvGSjmjlwXwXoQ%3D%3D; _pst=mephisto_512; __jda=122270672.16483548252141065341557.1648354825.1648375724.1648380443.8; TrackID=156ni-Rns82Dm_Gf8TUIz11rH0oyQVlgjZJ98elxk9rPcwdp4Qe6cpab2coHAn7332JM3e3DJVCA7S8qfpJne9mK40scW1PLrpfiXNGoZYkM; rkv=1.0; qrsc=2; wlfstk_smdl=yv6rr6d6ez9dxyaeqjptbxsh94in137z; shshshfp=d17d22c081f650863e82089d5da94c42; token=26e085ae7f46f176a97c7b43fb5d9ec5,3,915767; __tk=YSrRvShxXpayvpoSYcaEZU2EZUhFvUnRuDbTYzdnXci3YzqFuz2xYG,3,915767; shshshsID=e89474f1fec3363b2399b007824bd961_6_1648381716056; __jdb=122270672.16.16483548252141065341557|8.1648380443; thor=40D31776F41554A61809E01C578642CF828AEB06ABB7F308A35F0D87504A722FF5127D789CE92D7F0CB23326B46752C60E21EFC14CF1585D2B1E49BC1609191F71EDFC4A60145D9C3530E7DBDBB7691716EA1326CDC277AF108D91C7C1ADF5C36B1B6A83C6517157C88C97EBC8F3852A71079440A404C4D1905019515F04E2C9271652F6236230713935BA9D3B5B3E2F; 3AB9D23F7A4B3C9B=C3GCDWWOACMDHUKGF4J3NC2O33J2CZ5B6CK7KWISDI3BDVZ5C4NWYRBKSXJHF4RCDTXPXJ76DEEDMFQVT74CK3D6A4'
        c = {i.split("=")[0]:i.split("=")[1] for i in cookie.split("; ")}
        # selector = Selector(response)
        # try:
        #     texts = selector.xpath('//div[@class="category-item m"]/div[@class="mc"]/div[@class="items"]/dl/dd/a').extract()
        #     for text in texts:
        #         items = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a>', text)
        #         for item in items:
        #             if item[0].split('.')[0][2:] in key_word:
        #                 if item[0].split('.')[0][2:] != 'list':
        #                     yield Request(url='https:' + item[0], callback=self.parse_category)
        #                 else:
        #                     categoriesItem = CategoriesItem()
        #                     categoriesItem['name'] = item[1]
        #                     categoriesItem['url'] = 'https:' + item[0]
        #                     categoriesItem['_id'] = item[0].split('=')[1].split('&')[0]
        #                     yield categoriesItem
        #                     yield Request(url='https:' + item[0], callback=self.parse_list)
        # except Exception as e:
        #     print('error:', e)

        # 测试
        yield Request(url='https://list.jd.com/list.html?cat=1315,1343,9720',
                      headers={
                          "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"},
                      cookies=c,
                      callback=self.parse_list)

    def parse_list(self, response):
        """分别获得商品的地址和下一页地址"""
        meta = dict()
        meta['category'] = response.url.split('=')[1].split('&')[0]

        selector = Selector(response)
        texts = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div[@class="p-img"]/a').extract()
        print(texts)
        for text in texts:
            items = re.findall(r'<a target="_blank" href="(.*?)">', text)
            print(items)
            yield Request(url='https:' + items[0], callback=self.parse_product, meta=meta)

        # next page
        next_list = response.xpath('//a[@class="pn-next"]/@href').extract()
        if next_list:
            # print('next page:', Base_url + next_list[0])
            yield Request(url=Base_url + next_list[0], callback=self.parse_list)

    def parse_product(self, response):
        """商品页获取title,price,product_id"""
        ids = re.findall(r"venderId:(.*?),\s.*?shopId:'(.*?)'", response.text)
        if not ids:
            ids = re.findall(r"venderId:(.*?),\s.*?shopId:(.*?),", response.text)
        vender_id = ids[0][0]
        shop_id = ids[0][1]

        shopItem = ShopItem()
        shopItem['shopId'] = shop_id
        shopItem['venderId'] = vender_id
        shopItem['url1'] = 'http://mall.jd.com/index-%s.html' % (shop_id)
        try:
            shopItem['url2'] = 'https:' + \
                               response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/a/@href').extract()[0]
        except:
            shopItem['url2'] = shopItem['url1']

        if shop_id == '0':
            name = '京东自营'
        else:
            try:
                name = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/a//text()').extract()[0]
            except:
                try:
                    name = response.xpath('//div[@class="name"]/a//text()').extract()[0].strip()
                except:
                    try:
                        name = response.xpath('//div[@class="shopName"]/strong/span/a//text()').extract()[0].strip()
                    except:
                        try:
                            name = response.xpath('//div[@class="seller-infor"]/a//text()').extract()[0].strip()
                        except:
                            name = u'京东自营'
        shopItem['name'] = name
        shopItem['_id'] = name
        yield shopItem
