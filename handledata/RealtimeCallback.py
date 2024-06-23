import json
import pandas as pd
import sys
from collections import defaultdict
import client.sss as sss


class RealtimeCallback:
    def __init__(self):
        # 初始化一个默认字典，用于缓存每个URL的部分数据
        self.data_cache = defaultdict(str)

    def callback(self, url, data_str):
        # 将新的数据添加到缓存中
        if self.data_cache[url] == "" or self.data_cache[url] == None:
            self.data_cache[url] = data_str[6:]
        else:
            self.data_cache[url] += data_str

        while True:
            try:
                print(f"解析数据: {self.data_cache[url]}")
                # 解析缓存数据为JSON对象
                data = json.loads(self.data_cache[url])
                # 如果成功，处理数据并清空缓存
                self.process_data(data)
                self.data_cache[url] = ""
                break
            except json.JSONDecodeError as e:
                print(f"解析数据错误: {e}")
                # 查找错误位置
                idx = e.pos
                if idx < len(self.data_cache[url]):
                    # 分割缓存数据并保留未解析部分
                    self.data_cache[url] = self.data_cache[url][idx:]
                else:
                    break

    def process_data(self, data):
        if data['data'] is None or data['data'] == '':
            return
        # 提取trends数据
        trends = data['data']['trends']

        # 处理trends数据，保留日期时间和所有数据
        processed_data = []
        for trend in trends:
            # 分割字符串，保留所有部分
            parts = trend.split(',')
            processed_data.append(parts)

        # 创建pandas DataFrame
        # 注意：这里的列名需要根据实际数据结构进行调整
        df = pd.DataFrame(processed_data, columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount', 'VWAP'])
        
        main = sss.MyWindow(df)
        main.show()
        
