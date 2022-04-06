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
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    logging.getLogger("requests").setLevel(logging.INFO)  # 将requests的日志级别设成WARNING
    cookie = 'shshshfpa=be28660b-6131-0769-8ec8-1ade9c648007-1603759917; shshshfpb=y/jalvZTUAAKNf4L60nKm8Q==; __jdu=16037597411491093498440; TrackID=1n2rPc1GE908uAK4PBndcHXo3v4mBZow3OP3jp24xlXnbgMbCLVbKGCFvU-Jc6Hdfw5n__XVmmvZQgWIqKn1NrhggBzGpifvZbnMkojYkhm0; pinId=zaebSevvwiKZAQYe7tFpnA; ceshi3.com=103; __jdv=122270672|direct|-|none|-|1648441593748; areaId=19; PCSYCityID=CN_440000_440100_0; warehistory="65152667601,10027965377386,"; autoOpenApp_downCloseDate_autoOpenApp_autoPromptly=1648446049671_1; jcap_dvzw_fp=UbH8AL709IPyF8VuS6S_HJdsWdNpNiswXlYJVxqmB_BbMDrsyXHWboSB-PNczJS3rJSPoA==; ipLoc-djd=19-1601-50258-51885; wlfstk_smdl=q0964mzb6xknwzag7doj299v4n0mrvci; __jdc=76161171; __jda=76161171.16037597411491093498440.1603759741.1648702385.1648875720.53; mba_muid=16037597411491093498440; shshshfp=d4fc1cba0427246d5557720ddd208861; shshshsID=b9c87c998a349b8c64ce25ba84341ced_4_1648877225708; 3AB9D23F7A4B3C9B=24UEL5APDG2MJF5LWHH3TLYCXXGNF4YSV3LN4UBYMIMTVJG2QMD7IS44BFVUOGJZRJY4AQY2LWQAO4LXMBQ6D5WKKQ; TrackerID=e1-9BoWLo76BzD8u_VzxgOokeGL_AqN3_9g2_SKlm-2bIB2NViTvQl-7MKhly9wobMFaHhGkWFE2-GKksaqL2LCazk606_AtaBHM2w5z8yI; pt_key=AAJiR9_wADA-SCmcp3fJXx8kV_DMR9NwNQLMFpxpB14LPMHKRFe2BP-TQ0pZKoo-HR2iuDqTVfI; pt_pin=mephisto_512; pt_token=7jwo4uqf; pwdt_id=mephisto_512; sfstoken=tk01mcd591c5ca8sMysybHJXQ2tl0Vt3nqFJvs7xeqVZUF7KVBEjVOiJiZLk/SJYP2TK6ZtmlKwih6Mx2oWSoE+A1VFh; whwswswws=; wxa_level=1; retina=1; cid=3; wqmnx1=MDEyNjM1M3B3ZC8vL3IvcnJlaHRuMmwuaXMxIDQ0cGI1NlRsRylvNjY1YTMxRmZhYUI0UUVTKUYpSA==; jxsid=16488775551748193992; webp=1; __jdb=76161171.15.16037597411491093498440|53.1648875720; mba_sid=1648877225214673433676342238.2; visitkey=39862575624616266'
    c = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    ua = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"
    opt = Options()
    opt.add_argument('-headless')
    driver = webdriver.Chrome(chrome_options=opt)

    def __del__(self):
        JDSpider.driver.quit()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies={
                "pt_key": "AAJiR9_wADA-SCmcp3fJXx8kV_DMR9NwNQLMFpxpB14LPMHKRFe2BP-TQ0pZKoo-HR2iuDqTVfI",
                "pt_pin": "mephisto_512"}, callback=self.parse_category)

    def parse_category(self, response):
        """获取分类页"""
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
                      headers={"User-Agent": JDSpider.ua},
                      cookies=JDSpider.c,
                      callback=self.parse_list)

    def parse_list(self, response):
        """分别获得商品的地址和下一页地址"""
        meta = dict()
        meta['category'] = response.url.split('=')[1].split('&')[0]

        selector = Selector(response)
        texts = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div[@class="p-img"]/a').extract()
        for text in texts:
            items = re.findall(r'<a target="_blank" title="(.*?)" href="(.*?)">', text)
            yield Request(url='https:' + items[0][1].split('"')[0], headers={"User-Agent": JDSpider.ua},
                          cookies=JDSpider.c, callback=self.parse_product, meta=meta)

        # next page
        # next_list = response.xpath('//a[@class="pn-next"]/@href').extract()
        # if next_list:
        #     # print('next page:', Base_url + next_list[0])
        #     yield Request(url=Base_url + next_list[0], headers={"User-Agent": JDSpider.ua},
        #                   cookies=JDSpider.c, callback=self.parse_list)

    def parse_product(self, response):
        """商品页获取title,price,product_id"""
        JDSpider.driver.get(response.url)
        ids = re.findall(r"shopId=(.*?)&", JDSpider.driver.page_source)
        with open("./zz.log", 'a', encoding='utf-8') as f:
            f.write(f'{ids[0]}\n')
