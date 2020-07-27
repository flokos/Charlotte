# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from Charlotte.items import Hotel_link
from datetime import datetime
from scrapy.utils.response import open_in_browser
import re

class CharlotteSpider(scrapy.Spider):
   
    name = "Charlotte"
    allowed_domains = ["booking.com","booking.com/searchresults.el.html"]
    def __init__(self,destination=None, *args, **kwargs):
        super(CharlotteSpider, self).__init__(*args, **kwargs)
        #Pass destination as an argument of the spider class .
        self.destination = destination
        #Pass the time to the spider class
        self.now = datetime.now()
        #Pass a list to check for duplicates
        self.hotel_links = []
        self.avail_filters = []
        self.sel_filters = []

    def start_requests(self):
              #Fill the search form and request the new page .
              return [FormRequest("http://www.booking.com/searchresults.el.html",
                    formdata = {
                        'ss':self.destination,
                        'checkin_monthday':str(self.now.day),
                        'checkin_month':str(self.now.month),
                        'checkin_year':str(self.now.year),
                        'checkout_monthday':str(self.now.day+1),
                        'checkout_month':str(self.now.month),
                        'checkout_year':str(self.now.year),
                        'no_rooms':'1',
                        'group_adults':'1',
                        'group_children':'0',
                        'sb':'1',
                        'src':'index',
                        'src_elem':'sb',
                        'nflt':'1',
                        'sb_acc_types':'1',
                        'room1':'A',
                        'no_rooms':'1',
                        },
                    method="GET", 
                    callback = self.parse_filters,
                    dont_filter = True,
                            )]
           
    def parse(self, response):
        #Make an Hotels Item
        Hotel = Hotel_link()
        #For every hotel link in a page do ....
        for link in response.css('#hotellist_inner > div.sr_item'):
            #If current hotel was not on the previous page and it is not out of stock .
            if set(link.css('a.hotel_name_link.url > span.sr-hotel__name::text').extract()).issubset(self.hotel_links) == False:
                #Set Hotels Item (url and hotel name)
                Hotel['url'] = link.css('a.hotel_name_link.url::attr(href)').extract_first().replace(';','&')
                Hotel['name'] =  link.css('a.hotel_name_link.url > span.sr-hotel__name::text').extract_first().replace("\n","").encode('utf-8', 'ignore').replace('*',' star ')
                stars = link.css('i.stars')
                print stars
                rec = link.css('i.icon_deal_smart')
                if stars.extract_first() is not None:
                    print re.search(r'\d+',stars.css('span.invisible_spoken::text').extract_first()).group()
                    Hotel['stars'] = str(re.search(r'\d+',stars.css('span.invisible_spoken::text').extract_first()).group())
                else:
                    Hotel['stars'] = '0'
                if rec.extract_first() is not None:
                    Hotel['rec'] = '1'
                else:
                    Hotel['rec'] = '0'
                #Return the Hotels Item
                yield Hotel
        #If you are on the first page show the page to the user        
        if "offset="not in str(response.url):
            open_in_browser(response)
        #Next page url        
        next_page = str(response.css('#search_results_table > div.results-paging > a.paging-next::attr(href)').extract_first())
        #if next page button exists do ...
        if response.css('#search_results_table > div.results-paging > a.paging-next::attr(href)').extract_first() is not  None:
            
            #Pass the current hotel list to the next page to check for duplicates
            self.hotel_links.extend(response.css('a.hotel_name_link.url>span.sr-hotel__name::text').extract())
            #Go to the next page 
            yield scrapy.Request(url=str("http://www.booking.com"+next_page),callback=self.parse,dont_filter = True)
        else:
            #Show the page to the user
            open_in_browser(response)
            
    def parse_filters(self,response):
        #For every filter do ...
        for filters in response.css('div.filterbox'):
            print filters.css('div.filtercategory > h3::text').extract_first()+'-'*10
            #For every filter option do ...
            for filters_option in filters.css('a.filterelement'):
                #Update the available filters list 
                self.avail_filters.append([filters_option.css('::attr(href)').extract_first(),
                filters_option.css('span.filter_label::text').extract_first()])
                #Print the filter and the filter code
                print self.avail_filters[len(self.avail_filters)-1][1]  + ':' + str(len(self.avail_filters)-1)
        print 'Start crawling : start \n\n'
        print 'Applied filters :'
        #For every filter in the selected filters list do ...
        for filtr in self.sel_filters:
            #Print the filter
            print filtr.encode('utf-8')
        #If the selected filters list is not empty do ...
        if self.sel_filters:
            print 'To deselect a filter enter its number(new) again.'
        #Do_while
        while True:
            #Read user input
            user_input = raw_input('Choose a filter to be applied(enter the number next to the filter) :')
            #Print available filters
            print len(self.avail_filters)
            #If the user input is a number and this number is smallen than the length of the available filters list and bigger than zero .
            if user_input.isdigit() and int(user_input) < len(self.avail_filters) and int(user_input) >=0:
                #If the selected filter is in the selected filters list
                if any(self.avail_filters[int(user_input)][1] in s for s in self.sel_filters):
                    #Remove the filter from selected filters list
                    self.sel_filters.remove(self.avail_filters[int(user_input)][1])
                else:
                    #Put the filter in the selected filters list
                    self.sel_filters.append(self.avail_filters[int(user_input)][1])
                #Visit the new page with the filtered results
                yield scrapy.Request(url=str("http://www.booking.com"+self.avail_filters[int(user_input)][0]),
                callback=self.parse_filters,dont_filter = True)
                #Empty the avaiable filters list
                self.avail_filters = []
                #Get out of the while statement
                break
            #if the user enters the keyword 'start'
            if user_input == 'start':
                #Start crawling the hotels links 
                yield scrapy.Request(url=response.url,callback=self.parse,dont_filter = True)
                #Get out of the while statement
                break
            #Wrong input message     
            print 'Wrong Input!!! \n  Input should be an integer or the word start.'          