# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Hotel_link(scrapy.Item):
    #Hotel URL
    url = scrapy.Field()
    #Hotel Name
    name = scrapy.Field()
    #Hotel Stars
    stars = scrapy.Field()
    #Hotel reccommended or not.
    rec = scrapy.Field()
    pass
class Hotel(scrapy.Item):
    #HoteL name
    name = scrapy.Field()
    #Hotel longitute
    longtitude = scrapy.Field()
    #Hotel Lattitude
    lattitude = scrapy.Field()
    #General Rating
    rating = scrapy.Field()
    #Clean Rating
    cl_rating = scrapy.Field()
    #Comfort Rating
    comf_rating = scrapy.Field()
    #Location Rating
    loc_rating = scrapy.Field()
    #Services Rating
    serv_rating = scrapy.Field()
    #Staff Rating
    st_rating = scrapy.Field()
    #Quality/Price Rating
    qp_rating = scrapy.Field()
    #Wifi Rating
    wf_rating = scrapy.Field()
    #Number of Reviews
    no_reviews = scrapy.Field()
    #List containing the provisions of the hotel
    provisions = scrapy.Field()
    #Dict containing rooms info
    rooms = scrapy.Field()
    pass
