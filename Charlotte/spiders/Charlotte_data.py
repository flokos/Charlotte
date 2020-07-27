# -*- coding: utf-8 -*-
import scrapy
import re
import csv
from datetime import timedelta
from datetime import datetime
from Charlotte.items import Hotel
from scrapy.utils.markup import remove_tags

class CharlotteDataSpider(scrapy.Spider):
    
    name = "Charlotte_data"
    allowed_domains = ["Charlotte"]
    def __init__(self,load_csv=None,duration=None, *args, **kwargs):
        super(CharlotteDataSpider, self).__init__(*args, **kwargs)
        #Pass the input file origin as a spider argument
        self.load_csv = load_csv
        #Pass the duration of stay as a spider argument
        self.duration = duration
        #Pass the date/time as a spider argument
        self.now = datetime.now()
    def start_requests(self):
        #Set check in date as today
        checkin = self.now
        #Set check out day as the day after 'duration' days
        checkout = self.now + timedelta(days=int(self.duration))
        #Open the file containing the hotel links
        with open(self.load_csv,'rt') as f_r:
            reader = csv.reader(f_r, delimiter=',')
            #For every row in the file do ...
            for row in reader:
                #if the row is not the first row do ..
                if row[1] != 'url':
                    #Make the url to be visited(adjust date)
                    url = re.sub(r'checkin=\w+\-\w+\-\w+\&checkout=\w+\-\w+\-\w+',r'checkin='+checkin.strftime('%Y-%m-%d')+'&checkout='+checkout.strftime('%Y-%m-%d'),str(row[1]))
                    #Visit the created url
                    yield scrapy.Request(url=str("http://www.booking.com"+url),callback=self.parse,dont_filter = True)
        #Close the file containing the hotel links     
        f_r.close()
    def parse(self, response):
        #Make a Hotel() item
        current_hotel = Hotel()
        #Get Hotel name
        current_hotel['name'] = response.css('#hp_hotel_name::text').extract_first().replace('\n','').encode('utf-8')
        #Get Hotel Geodata
        geodata = response.css('span.hp_address_subtitle::attr(data-bbox)').extract_first().split(',')
        #Get Hotel Lattitude
        current_hotel['lattitude'] = geodata[1]
        #Get Hotel longtitude
        current_hotel['longtitude'] = geodata[2]
        #If the ratings table exists do ...
        if response.css('#js--hp-gallery-scorecard::attr(data-review-score)').extract_first() is not None:
            #Get Hotel Rating
            current_hotel['rating'] = int(float(response.css('#js--hp-gallery-scorecard::attr(data-review-score)').extract_first())*10)
        if response.css('#review_list_score_breakdown > li > div.score_bar > div.score_bar_value::attr(data-score)').extract():
            #Get secondary hotel ratings
            ratings = response.css('#review_list_score_breakdown > li > div.score_bar > div.score_bar_value::attr(data-score)').extract()
            #Get Hotel 'clean' rating
            current_hotel['cl_rating'] = ratings[0]
            #Get Hotel 'comfort' rating
            current_hotel['comf_rating'] = ratings[1]
            #Get Hotel 'location' rating
            current_hotel['loc_rating'] = ratings[2]
            #Get Hotel 'Services' rating
            current_hotel['serv_rating'] = ratings[3]
            #Get hotel 'Staff' rating
            current_hotel['st_rating'] = ratings[4]
            #Get hotel 'Quality/Price' rating
            current_hotel['qp_rating'] = ratings[5]
            #Get hotel 'Wifi' rating
            current_hotel['wf_rating'] = ratings[6]
        #if the number of reviews is visible do ...
        if response.css('strong.count::text').extract_first() is not None:
            #Get hotel number of reviews
            current_hotel['no_reviews'] = response.css('strong.count::text').extract_first().replace('\n','')
        #if the provisions of the hotel are visible do ...
        if response.css('#hotel_main_content > div.hp_hotel_description_hightlights_wrapper > div.hotel_description_wrapper_exp.hp-description > div.hp_desc_important_facilities > div.important_facility.hp-desc-facility') is not None:
            #Get Hotel provisions
            current_hotel['provisions'] = []
            for provision in response.css('#hotel_main_content > div.hp_hotel_description_hightlights_wrapper > div.hotel_description_wrapper_exp.hp-description > div.hp_desc_important_facilities > div.important_facility.hp-desc-facility'):
                label = provision.css('i::attr(class)').extract_first().split(' ')
                if label[0] not in current_hotel['provisions']:
                    current_hotel['provisions'].append(label[0].replace('bicon-','').replace('\n',''))
        #Get number of different types of rooms
        no_rtypes = len(response.css('td.roomType'))
        #if there are available rooms 
        rooms = {}
        if no_rtypes > 0:
            #For every room type do ...
            j=1
            for i in range(1,no_rtypes+1):
                #Get room type class
                room_class = u'room_loop_counter'+ str(i)
                #For every room in this room type do ...
                for room in response.css('tr'+'.'+room_class):
                    #if you are in the correct cell(of the table) do ...
                    if (room_class + u'\nextendedRow\n' in room.css('::attr(class)').extract() or room_class+u'\nmaintr\n' in room.css('::attr(class)').extract())==False:  
                        #Make a list that contains the current room data 
                        current_room = [None]*9
                        #Default value of prepayment
                        current_room[5] = '1'
                        #Default value of no_returns
                        current_room[6] = '1'
                        #Get current 'max people per roon' for the current room
                        current_room[0] = room.css('td.roomMaxPersons::attr(data-occupancy-for-tracking)').extract_first()
                        #Get current room 'policies'
                        #If free breakfast is provided do ...
                        if room.css('td.ratepolicy > div.hp-rt__policy > ul.hp-rt__policy-list > li > span.bicon-coffee.mp-icon.meal-plan-icon.hp_rc_breakfast_clarity_track'):
                            current_room[1] = '1'
                        #if free half-board is provided do ...
                        if room.css('td.ratepolicy > div.hp-rt__policy > ul.hp-rt__policy-list > li > span.bicon-forkknife.mp-icon.meal-plan-icon-small'):
                            current_room[2] = '1'
                        #If there is a free cancel policy
                        if room.css('td.roomMultiRoomPrice > div.roomDefaultUse > select.b_free_cancel'):
                            current_room[3] = '1'
                            #If you have a free cancel policy no_returns does not exist 
                            current_room[6] = None
                        #if there is a flexible cancel policy and no prepayment is neede
                        if u' \nSEMI FLEX - \u03c0\u03bb\u03b7\u03c1\u03ce\u03bd\u03b5\u03c4\u03b5 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7 \u03b4\u03b9\u03b1\u03bc\u03bf\u03bd\u03ae \u03c3\u03b1\u03c2\n ' in room.css('td.ratepolicy > div.hp-rt__policy > ul.hp-rt__policy-list > li.hp-rt__policy__item > span::text').extract():
                            current_room[4] = '1'
                            current_room[5] = None
                            #If you have a semi-flex cancel policy no_returns does not exist
                            current_room[6] = None
                        #if there is a flexible cencel policy but prepayment is needed
                        if u' \nSemi flex\n ' in room.css('td.ratepolicy > div.hp-rt__policy > ul.hp-rt__policy-list > li.hp-rt__policy__item > span::text').extract():
                            current_room[4] = '1'
                            current_room[5] = '1'
                            #If you have a semi-flex cancel policy no_returns does not exist
                            current_room[6] = None
                        #Get current room 'price'
                        current_room[7] = room.css('td.roomPrice > div.hp-rt-room-price > strong::attr(data-price-without-addons)').extract()
                        #Get current room 'provisions'
                        current_room[8] = response.css('tr.'+room_class+'.maintr > td.roomType.room-type-container.rt__room-detail.rt__room-detail--legibility > span > span.highlighted_facilities_reinforcement > div.iconfont_wrapper > div.rt-all-facilities-hidden > span::attr(data-name-en)').extract()
                        #Update the dictionary containing the hotel rooms data
                        rooms.update({j:current_room})
                        #Update counter that shows the position in the dictionary 
                        j=j+1
        #Pass the rooms dicionary to the 'rooms' element of the hotel item .                
        current_hotel['rooms'] = rooms
        #Return the hotel item
        yield current_hotel