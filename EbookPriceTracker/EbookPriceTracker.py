import sqlite3
from EBookDB import BookDatabase
from PriceTracker import EBookPriceTracker

if __name__=='__main__':

    book_lists = {
        "B07BDFDKD4": "救赎者",
        "B07BDJT8SX": "知更鸟"
    }

    tracker = EBookPriceTracker(book_lists)
    tracker.UpdatePrice()