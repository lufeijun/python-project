import scrapy
import json

from lufeijun.items import LufeijunItem

# 在执行 scrapy crawl demo 开始爬取后，所有中间件中的 spider 参数，就是指的这个类

class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["www.baidu.com"]
    start_urls = [
        "http://192.168.0.47:8000/info?page=1",
        "http://192.168.0.47:8000/info?page=2",
        "http://192.168.0.47:8000/info?page=3",
        "http://192.168.0.47:8000/info?page=4",
        "http://192.168.0.47:8000/info?page=5",
    ]

    def parse(self, response):
        list = json.loads( response.body.decode() )
        for value in list:
            item = LufeijunItem(
                age= value["age"],
                name = value["name"],
            )
            yield item

    def sayHello(self):
        print("hello world")    
