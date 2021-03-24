from EBookDB import BookDatabase
from bs4 import BeautifulSoup
import requests
import re

class EBookPriceTracker(object):

    url = "https://www.amazon.cn/s/ref=nb_sb_noss?url=search-alias%3Ddigital-text&field-keywords="

    def __init__(self, book_lists):
        self.db = BookDatabase()
        self.db.init_database()
        self.db.book_lists = book_lists

    def RunPriceTracker(self):
        self.UpdatePrice()
        self.Alert()

    def UpdatePrice(self):
        for book_asin in self.db.book_lists.keys():
            self._updateBookPrice(book_asin)

    def Alert(self):
        pass

    def _updateBookPrice(self, asin):
        url = self.url + asin
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        html = requests.get(url, headers = headers)
        if (html.status_code != 200):
            return

        html.encoding = "utf-8"
        bshtml = BeautifulSoup(html.text, "html.parser")

        divs = bshtml.find_all("div", id="atfResults")
        book_lis = [div.ul for div in divs]
        
        for book_li in book_lis:            
            str_price = book_li.find("span", class_="a-size-base a-color-price s-price a-text-bold").string
            tmp_pattern = re.compile("\d+\.?\d*")
            prices = tmp_pattern.findall(str_price)
            if len(prices):
                self.db.insert_line(asin, prices[0])

            
        
    

    