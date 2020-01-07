# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
from pathlib import Path
from datetime import datetime

class Day027HwScrapyItemPipeline(object):
    def process_item(self, item, spider):
        return item


class JSONPipeline(object):
    def open_spider(self, spider): #建立資料庫連線:開啟爬蟲後要做的動作
        self.start_crawl_datetime = datetime.now().strftime('%Y%m%dT%H-%M-%S') #注意檔名若使用 '%Y%m%dT%H:%M:%S' 不可，檔名中不可有冒號

        # 在開始爬蟲的時候建立暫時的 JSON 檔案
        # 避免有多筆爬蟲結果的時候，途中發生錯誤導致程式停止會遺失所有檔案
        self.dir_path = Path(__file__).resolve().parents[1] / 'crawled_data'
        self.runtime_file_path = str(self.dir_path / '.tmp.json.swp')
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)
        spider.log('Create temp file for store JSON - {}'.format(self.runtime_file_path))

        # 設計 JSON 存的格式為
        # [
        #  {...}, # 一筆爬蟲結果
        #  {...}, ...
        # ]
        self.runtime_file = open(self.runtime_file_path, 'w+', encoding='utf8')
        self.runtime_file.write('[\n')
        self._first_item = True

    def process_item(self, item, spider): #處理資料
        # 把資料轉成字典格式並寫入文件中
        if not isinstance(item, dict): # isinstance() 判斷item是否為字典，若不是，dict()轉為字典
            item = dict(item)

        if self._first_item:
            self._first_item = False
        else:
            self.runtime_file.write(',\n')

        self.runtime_file.write(json.dumps(item, ensure_ascii=False)) #json默認中文為ascii編碼，須關閉，以顯示中文
        return item

    def close_spider(self, spider): #關閉資料庫連線
        self.end_crawl_datetime = datetime.now().strftime('%Y%m%dT%H-%M-%S')

        # 儲存 JSON 格式
        self.runtime_file.write('\n]')
        self.runtime_file.close()
        
        # 將暫存檔改為以日期為檔名的格式
        self.store_file_path = self.dir_path / '{}-{}.json'.format(self.start_crawl_datetime,
                                                                   self.end_crawl_datetime)
        self.store_file_path = str(self.store_file_path)
        os.rename(self.runtime_file_path, self.store_file_path)
        spider.log('Save result at {}'.format(self.store_file_path))
    
#到settings.py啟用ITEM_PIPLINES 項目