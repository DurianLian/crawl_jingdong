# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jingdong.items import JingdongItem
import urllib.request
import re


class JdSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://www.jd.com/']
    # allow为空，爬取满足域名的所有网址
    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = JingdongItem()
            #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
            #item['name'] = response.xpath('//div[@id="name"]').get()
            #item['description'] = response.xpath('//div[@id="description"]').get()
            thisurl = response.url
            pat = 'item.jd.com/(.*?).html'
            x = re.search(pat,thisurl)
            if(x):
                thisid = re.compile(pat).findall(thisurl)[0]
                # print(thisid)
                title = response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').extract()
                shop = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()').extract()
                shoplink = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/@href').extract()
                thisidurl = 'http://item.jd.com/' + thisid + '.html'
                itemdata = urllib.request.urlopen(thisidurl).read().decode('utf-8','ignore')
                pat1 = 'venderId:(.*?),'
                pat2 = 'cat: \[(.*?)\],'
                venderid = re.compile(pat1).findall(itemdata)
                catid = re.compile(pat2).findall(itemdata)
                # new_shoplink = 'http://' + shoplink[0]
                # print(title)
                # print(shop)
                # print(shoplink)
                # print(venderid,catid)
                if len(venderid) and len(catid):
                    # priceurl='https://p.3.cn/prices/mgets?callback=jQuery964768&type=1&area=16_1315_1316_0&pdtk=&pduid='+thisid+'&pdpin=&pin=null&pdbp=0&skuIds=J_23948466394%2CJ_27623852091%2CJ_41634446399%2CJ_34556083307%2CJ_32418252597%2CJ_40055918437&ext=11100000&source=item-pc'
                    priceurl = 'https://c0.3.cn/stock?skuId='+thisid+'&area=16_1315_1316_0&venderId='+venderid[0]+'&buyNum=1&choseSuitSkuIds=&cat='+catid[0]+'&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=15837572578341093748173&ch=1&callback=jQuery3837695'
                    # print(priceurl)
                    pricedata = urllib.request.urlopen(priceurl).read().decode('utf-8','ignore')
                    # print(pricedata)
                    commenturl = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+thisid+'&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&rid=0&fold=1'
                    commentdata = urllib.request.urlopen(commenturl).read().decode('utf-8')
                    pricepat = '"jdPrice":{"p":"(.*?)",'
                    commentpat = '"goodRateShow":(.*?),'
                    price = re.compile(pricepat).findall(pricedata)
                    comment = re.compile(commentpat).findall(commentdata)
                    # 判断商品信息是否有空的，商品信息有空的就不不需要爬取了
                    if len(title) and len(shop) and len(shoplink) and len(price) and len(comment):
                        print('商品标题：'+title[0].strip())
                        print('商品链接：'+'https://item.jd.com/'+thisid+'.html')
                        print('店铺名称：'+shop[0])
                        print('店铺链接：'+'http:'+shoplink[0])
                        print('商品价格：'+price[0])
                        print('商品好评度：'+comment[0])
                        print('-----------------------------')
                    else:
                        pass
                else:
                    pass

            return item
        except Exception as e:
            pass
            # print(e)
