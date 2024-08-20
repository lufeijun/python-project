# scrapy 爬虫


## 生成一个 demo spider 

```
1、创建项目
scrapy startproject lufeijun

2、进入项目目录
cd lufeijun

3、生成一个 spider

scrapy genspider demo http://demo.com

4、执行爬虫

scrapy crawl demo

```


## 当前分支

爬取自己的数据，通过返回的 json 数据，生成 Excel 

```
1、修改 DemoSpider ： 爬取连接

2、修改 LufeijunItem ：调整数据结构

3、修改 LufeijunPipeline ：调整保存后的 Excel 数据

```