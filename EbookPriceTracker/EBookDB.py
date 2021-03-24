import sqlite3
import datetime
import os

class BookDatabase(object):

    db_file = "ebookdb.db"
    booklists = {}

    def __init__(self):
        pass

    def init_database(self):
        b_exists = os.path.isfile(self.db_file)
        if b_exists:
            return

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE EBOOKPRICE
                        (ASIN   TEXT     NOT NULL,
                        DATE    TEXT    NOT NULL,
                        PRICE   REAL    NOT NULL,
                        PRIMARY KEY (ASIN, DATE));''')
        conn.commit()
        conn.close()

    def insert_line(self, asin, price):
        b_book_exists = self.booklists.has_key(asin)
        if not b_book_exists:
            return

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EBOOKPRICE VALUES (?, ?, ?)", (asin, datetime.datetime.now(), price))
        conn.commit()
        conn.close()

    def read_price(self, asin):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        statm = "SELECT PRICE FROM EBOOKPRICE WHERE ASIN = %s ORDER BY DATE DESC" % asin
        cursor.execute(statm)
        for item in cursor:
            lasted_price = item[0]
            break

        statm = "SELECT AVG(PRICE) FROM EBOOKPRICE WHERE ASIN = %s" % asin
        cursor.execute(statm)
        for item in cursor:
            avg_price = item[0]
            break

        conn.commit()
        conn.close()

        return [avg_price, lasted_price]
