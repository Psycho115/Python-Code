# -*- coding: UTF-8 -*-


from bs4 import BeautifulSoup
import requests
import re
import markup


class ItemBase(object):
    

    def __init__(self):
        
        self.itemfields = {}


    def Field(self, fieldname):
        
        self.itemfields[fieldname] = u""


    def SetValue(self, fieldname, fieldvalue):
        
        if self.itemfields.has_key(fieldname):
            self.itemfields[fieldname] = fieldvalue
        else:
            print fieldname
            print " key not found\n"


    def GetValue(self, fieldname):
        
        if self.itemfields.has_key(fieldname):
            return self.itemfields.get(fieldname)
        else:
            return None


    def LogXml(self, xmlfile):
        
        xmlfile.write("\t<item>\n")
        for key in self.itemfields.keys():
            xmlfile.write("\t\t<%s>\n\t\t\t" % (key))
            xmlfile.write(self.itemfields.get(key).encode("utf-8"))
            xmlfile.write("\n\t\t</%s>\n" % (key))
        xmlfile.write("\t</item>\n")


class Item(ItemBase):
    

    def __init__(self):
        
        ItemBase.__init__(self)

        self.Field("title")
        self.Field("author")
        self.Field("link")
        self.Field("pic")
        self.Field("price")


class XMLFeed(object):
    
    
    def __init__(self, filename):
        
        self.xmlfile = open(filename, "wb")


    def Finished(self):
        
        self.xmlfile.close()


    def __del__(self):
        
        if not self.xmlfile.closed:
            self.xmlfile.close()


    def WriteXML(self, mylist):
        
        self.xmlfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        self.xmlfile.write("<Items>\n")
        for item in mylist:
            item.LogXml(self.xmlfile)
        self.xmlfile.write("</Items>\n")


class HTMLFeed(object):
    
    
    def __init__(self, filename):
        
        self.htmlfile = open(filename, "wb")


    def Finished(self):
        
        self.htmlfile.close()


    def __del__(self):
        
        if not self.htmlfile.closed:
            self.htmlfile.close()


    def WriteXML(self, mylist):
        
        self.xmlfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        self.xmlfile.write("<Items>\n")
        for item in mylist:
            item.LogXml(self.xmlfile)
        self.xmlfile.write("</Items>\n")


class DoubanSpider:
    
    
    def __init__(self):
        
        self.url_list = ["https://www.amazon.cn/gp/feature.html/ref=sa_menu_kindle_l3_f126758?ie=UTF8&docId=126758"]
        self.item_list = []


    def Request(self, url):
        
        html = requests.get(url)
        html.encoding = "utf-8"
        self.bshtml = BeautifulSoup(html.text, "html.parser")


    def Parse(self, url):
        
        divs = self.bshtml.find_all("div", id=re.compile("fluid asin s9a\d"))
        book_divs = [div.div.div for div in divs]
        
        for book_div in book_divs:
            
            item = Item()
            price = book_div.find("span", class_="s9Price a-color-price a-size-base").string
            item.SetValue("price", re.search(r'(\d+.\d+)', price).group(0))
            item.SetValue("title", book_div.a["title"])
            item.SetValue("link", "http://www.amazon.cn" + book_div.a["href"])
            item.SetValue("author", book_div.find("div", class_="a-row a-size-small").string)
            item.SetValue("pic", book_div.a.div.div.img["src"])
            self.item_list.append(item)


    def ProcessItems(self):
        
        self.item_list.sort(lambda item1, item2: cmp(float(item1.GetValue("price")), float(item2.GetValue("price"))))


    def LogItems(self, filename):

        xml = XMLFeed(filename)
        xml.WriteXML(self.item_list)
        xml.Finished()
        

    def Crawl(self):
        
        for url in self.url_list:
            self.Request(url)
            self.Parse(url)

        self.ProcessItems()
        self.LogItems("doubanitems.xml")
