# -*- coding: UTF-8 -*-


from flighttools import FlightSpider_ctrip


if __name__=='__main__':
    
    dates = [u"2016-08-01",u"2016-08-02",u"2016-08-03"]
    flights = ["HU"]
    ctripspider = FlightSpider_ctrip(dates,flights)

    ctripspider.Crawl()