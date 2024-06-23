import requests
import threading
from queue import Queue

class StreamListener:
    def __init__(self, callback_instance):
        self.queues = {}  # 初始化队列字典
        self.lock = threading.Lock()  # 初始化线程锁
        self.threads = []  # 存储线程的列表
        self.callback = callback_instance  # 设置回调函数实例

    def start_listening(self, urls):
        for url in urls:
            self.add_url(url)  # 添加URL并启动监听

        for thread in self.threads:
            thread.join()

    def _listen_to_stream(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            with requests.get(url, headers=headers, stream=True) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            data = line.decode('utf-8').strip()
                            
                            # 立即处理每行数据
                            with self.lock:  # 确保线程安全
                                self.queues[url].put(data)
                            # 立即调用callback处理这行数据
                            self.callback.callback(url, data)
                            # print(f"Received data: {data}")
                else:
                    print(f"Failed to fetch data from {url}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    def get_data(self, url):
        data = []
        with self.lock:  # 确保线程安全
            while not self.queues[url].empty():
                data.append(self.queues[url].get())
        return data

    def add_url(self, url):
        print(f"Add url {url}")
        with self.lock:
            if url not in self.queues:
                self.queues[url] = Queue()  # 为新URL创建队列

        # 启动监听线程
        thread = threading.Thread(target=self._listen_to_stream, args=(url,))
        thread.start()
        self.threads.append(thread)
