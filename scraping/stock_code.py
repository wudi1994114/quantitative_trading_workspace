from enum import Enum

class StockCode(Enum):
    """
    Enum class for stock codes, including area code, stock code, and stock name in Chinese.
    """
    sh_600000 = ("600000", "sh", "上海浦东发展银行")
    sh_600519 = ("600519", "sh", "贵州茅台")
    sh_603259 = ("603259", "sh", "药明康德")
    sz_000001 = ("000001", "sz", "平安银行")
    sz_000002 = ("000002", "sz", "万科")

    def __init__(self, code, area, stock_name):
        self._code = code
        self._area = area
        self._stock_name = stock_name

    @property
    def code(self):
        return self._code

    @property
    def area(self):
        return self._area

    @property
    def stock_name(self):
        return self._stock_name
    
    @property
    def full_code(self):
        return f"{self.area}{self.code}"


    def __str__(self):
        return f"Area: {self.area}, Code: {self.code}, Name: {self.stock_name}"
    


    @classmethod
    def get_by_stock_name(cls, stock_name):
        """
        Get the enum instance by stock name.
        """
        for stock in cls:
            if stock.stock_name == stock_name:
                return stock
        return None

    @classmethod
    def iterate_all(cls):
        """
        Iterate over all enum instances.
        """
        return list(cls)
    
