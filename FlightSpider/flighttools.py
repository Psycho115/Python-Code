# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import time
import os


class ItemBase(object):
    

    def __init__(self):
        
        self.itemfields = {}


    def Field(self, fieldname):
        
        self.itemfields[fieldname] = ""


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

        self.Field("flight")
        self.Field("date")
        self.Field("arrtime")
        self.Field("deptime")
        self.Field("price")
        self.Field("checktime")


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


class DatabaseFeed(object):
    
    
    def __init__(self, filename, flights):
        
        if os.path.exists(filename):
            self.dbfile = sqlite3.connect(filename)
            print "{0} connected!".format(filename)
            return

        self.dbfile = sqlite3.connect(filename)
        print "{0} created and connected!".format(filename)
        for flight in flights:
            self.dbfile.execute("create table {0} ( \
                                 CheckTime TEXT, \
                                 DepartureDate TEXT, \
                                 ArriveTime TEXT, \
                                 DepartureTime TEXT, \
                                 Price integer)".format(flight))
        self.dbfile.commit()


    def Finished(self):
        
        self.dbfile.close()
        print "Database disconnected!" 


    def Clear(self, flights):
        
        for flight in flights:
            self.dbfile.execute("Delete From {0}".format(flight))
        self.dbfile.commit()


    def LogItemIntoDatabase(self, item):
        
        flight = item.GetValue("flight")
        checktime = item.GetValue("checktime")
        depdate = item.GetValue("date")
        arrtime = item.GetValue("arrtime")
        deptime = item.GetValue("deptime")
        price = item.GetValue("price")
        data = (checktime, depdate, arrtime, deptime, price)

        self.dbfile.execute("insert into {0} values (?,?,?,?,?)".format(flight), data)
        self.dbfile.commit()

    
    def GetRow(self, flight, depdate, checktime="all"):

        if checktime=="all":
            script = "SELECT * FROM {0} WHERE DepartureDate == \"{1}\"".format(flight, depdate)
        else:
            script = "SELECT * FROM {0} WHERE DepartureDate == \"{1}\" AND CheckTime == \"{2}\"".format(flight, depdate, checktime)
        
        cursor = self.dbfile.execute(script)
        for row in cursor:
            return row


class FlightSpider_ctrip:
    
    depcity = "HGH"
    arrcity = "SIA"
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights"
    
    def __init__(self, dates, flightsCompany):
        
        self.dates = dates
        self.GeneratePostList(dates)
        self.flightsCompany = flightsCompany
        self.flights_set = set([])
        self.item_list = []


    def Get_CK(self, ckgetter_url):

        html = requests.get(ckgetter_url)
        print html.status_code
        html.encoding = "gb2312"
        bshtml = BeautifulSoup(html.text, "html.parser")
        script = bshtml.html.body.script.string
        ck_result = re.search("IsNearAirportRecommond=0&CK=(.*)\"",script)
        return ck_result.group(1)


    def GeneratePostList(self, dates):
      
        self.post_list = []
        for date in dates:
            ckgetter_url = "http://flights.ctrip.com/booking/{0}-{1}-day-1.html?DDate1={2}".format(self.depcity, self.arrcity, date)
            current_CK = self.Get_CK(ckgetter_url)
            postdata = {"DCity1":self.depcity,
                        "ACity1":self.arrcity,
                        "SearchType":"S",
                        "DDate1":date,
                        "IsNearAirportRecommond":"0",
                        "CK":current_CK}
            self.post_list.append(postdata)


    def Request_Json(self, post):
        
        content = requests.post(self.url, post)
        print content.status_code
        content.encoding = "gb2312"
        self.content_json = json.loads(content.text)


    def Parse_Json(self, url):
        
        flightresults = self.content_json["fis"]

        for flightresult in flightresults:
            
            for flight in self.flightsCompany:
                
                if flightresult["alc"] != flight:
                    continue
                    
                item = Item()
                self.flights_set.add(flightresult["fn"])
                item.SetValue("flight", flightresult["fn"])
                item.SetValue("date", flightresult["dt"].split()[0])
                item.SetValue("arrtime", flightresult["at"].split()[1])
                item.SetValue("deptime", flightresult["dt"].split()[1])
                item.SetValue("price", flightresult["lp"])
                item.SetValue("checktime", time.strftime("%Y-%m-%d",time.localtime(time.time())))
                
                self.item_list.append(item)


    def ProcessItems_Database(self, filename):
        
        db = DatabaseFeed(filename, self.flights_set)
        for flight in self.flights_set:
            for date in self.dates:
                row = db.GetRow(flight,date)
                if row:
                    print flight
                    print row
                else:
                    print flight
                    print "None"
        
        db.Finished()



    def LogItems_Database(self, filename):

        db = DatabaseFeed(filename, self.flights_set)
        for item in self.item_list:
            db.LogItemIntoDatabase(item)

        db.Finished()


    def ClearDatabase(self, filename):
            
        db = DatabaseFeed(filename, self.flights_set)
        db.Clear(self.flights_set)
        print "database cleared!"

        db.Finished()
        

    def Crawl(self):
        
        for post in self.post_list:
            self.Request_Json(post)
            self.Parse_Json(self.url)
        
        self.LogItems_Database("flight_db.db")
        self.ProcessItems_Database("flight_db.db")
        self.ClearDatabase("flight_db.db")
