# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook

class LufeijunPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["姓名", "年龄"])
        self.file_name = "test.xlsx"

    def process_item(self, item, spider):
        line = [item['name'], item['age']]
        self.ws.append(line)
        self.wb.save(self.file_name)
        return item
    
    def close_spider(self, spider):
        # 关闭
        self.wb.close()