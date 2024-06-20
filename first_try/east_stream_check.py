import requests
import time

def get_stream_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with requests.get(url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    # 处理每一行数据
                    data = line.decode('utf-8')
                    print(data)
        else:
            print(f"Failed to fetch data, status code: {response.status_code}")

url = 'http://69.push2.eastmoney.com/api/qt/stock/trends2/sse?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f17&fields2=f51,f52,f53,f54,f55,f56,f57,f58&mpi=1000&ut=fa5fd1943c7b386f172d6893dbfba10b&secid=1.603259&ndays=1&iscr=0&iscca=0&wbp2u=|0|0|0|web'

get_stream_data(url)