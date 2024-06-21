import requests
import threading
import pandas as pd
from queue import Queue


class StreamListener:
    def __init__(self):
        self.queues = []
        self.lock = threading.Lock()

    def start_listening(self):
        threads = []
        for url in self.urls:
            thread = threading.Thread(
                target=self._listen_to_stream, args=(url,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def _listen_to_stream(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with requests.get(url, headers=headers, stream=True) as response:
            if response.status_code == 200:
                buffer = ''
                for line in response.iter_lines():
                    if line:
                        buffer += line.decode('utf-8') + '\n'  # 将每行数据添加到缓冲区

                        # 假设每个数据包以换行符分隔，可以根据实际情况调整
                        if buffer.endswith('\n'):
                            # 处理每个完整的数据包
                            data = buffer.strip()
                            self.queues[url].put(data)  # 将数据包添加到队列中
                            self.callback(url, data)  # 调用回调函数
                            buffer = ''  # 清空缓冲区
            else:
                print(f"Failed to fetch data from {
                      url}, status code: {response.status_code}")

    def get_data(self, url):
        data = []
        while not self.queues[url].empty():
            data.append(self.queues[url].get())
        return data

    def add_url(self, url):
        with self.lock:
            if url not in self.queues:
                self.queues[url] = Queue()
                thread = threading.Thread(
                    target=self._listen_to_stream, args=(url,))
                thread.start()
