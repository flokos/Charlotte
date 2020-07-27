# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#Import needed libraries
import datetime
import time
import os
import csv
#Import Hotel_link and Hotel Items from items.py
from Charlotte.items import Hotel_link,Hotel



class CharlottePipeline(object):
    def __init__(self):
        #Pass the time to all functions
        self.now = datetime.datetime.now()
    def process_item(self, item, spider):
        #if the item processed is a Hotels Item do ...
        if isinstance(item,Hotel_link):
            #Handle the Hotel_link Item
            return self.store_Hotel_links(item,spider)
        if isinstance(item,Hotel):
            #Handle the hotel Item
            return self.store_Hotel(item,spider)
        return item
    def store_Hotel_links(self,item,spider):
        #Open the file that contains the hotels 
        with open('Hotel_links'+self.now.strftime('_%Y_%m_%d')+'.csv', 'ab') as f_w:
            dw = csv.DictWriter(f_w, ('name','url','stars','rec','date'),delimiter=',',dialect='excel')
            #if the Hotels csv file is empty write the header on the file
            if  os.stat('Hotel_links'+self.now.strftime('_%Y_%m_%d')+'.csv').st_size == 0:
                dw.writeheader()
            #Write the Hotel Item's contents on a new line in the hotels csv file 
            dw.writerow(item)
        #Close the file
        f_w.close()
        pass
    def store_Hotel(self,item,spider):
        #Open the file that containg the hotel links 
        with open('Hotels_data'+self.now.strftime('_%Y_%m_%d_%H_%M')+'.csv','ab') as f_w:
            dw = csv.DictWriter(f_w, ('name','longtitude','lattitude','rating','cl_rating','comf_rating','loc_rating','serv_rating','st_rating','qp_rating','wf_rating','no_reviews','provisions','rooms'),delimiter='\t')
            #if file is empty write the header on the file
            if  os.stat('Hotels_data'+self.now.strftime('_%Y_%m_%d_%H_%M')+'.csv').st_size == 0:
                dw.writeheader()
            #Write the Room Item's contents to a new line in the current hotel csv file
            dw.writerow(item)
        #Close the file
        f_w.close()
        pass