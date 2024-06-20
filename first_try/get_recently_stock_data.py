import requests
from bs4 import BeautifulSoup


def get_stock_price(stock_code):
    url = f"http://quote.eastmoney.com/{stock_code}.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 确保正确解析中文内容

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 打印HTML内容
        print(response.text)
        # 根据网页结构查找实时价格的数据标签，以下是一个示例，需要根据实际网页结构调整
        price_tag = soup.find('span', class_='price_down')  # 假设价格在class为price的div中
        if price_tag:
            price = price_tag.text.strip()
            return price
        else:
            return "Price tag not found"
    else:
        return f"Failed to fetch data, status code: {response.status_code}"


if __name__ == "__main__":
   stock_codes = ['603259']  # 添加你要监控的股票代码
   for stock_code in stock_codes:
       price = get_stock_price(stock_code)
       print(f"The latest price of {stock_code} is {price}")
